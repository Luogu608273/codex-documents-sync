"""Create the CV-8 Mon3tr adaptation and verify roster, tiles and ranges."""
import copy
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[1]


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def save(name, value):
    (BASE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


original = read(BASE / "original.json")
job = copy.deepcopy(original)
job["minimum_required"] = "v6.18.0"
box = {o["id"]: o for o in read(ROOT / "data/operators-2026-11-14.json")}
chars = read(BASE / "character_table.json")
skills = read(BASE / "skill_table.json")
ranges = read(BASE / "range_table.json")
mapdata = read(BASE / "map.json")
stage = read(BASE / "stage.raw.json")
assert original["stage_name"] == mapdata["stageId"] == "act28side_08"
assert (mapdata["width"], mapdata["height"]) == (13, 9)

job["doc"]["title"] = "CV-8 告别往昔｜Mon3tr一技能替换流明（待实测）"
job["doc"]["details"] = (
    original["doc"]["details"]
    + "\n\n本地修改：2026-11-14，基于prts://87122；未改动线上原作业。\n"
    "流明替换为自有医疗干员Mon3tr，保持原位置MAA坐标(10,5)、朝左。"
    "Mon3tr精二60、1技能专三、X模组三级；1技能由游戏自动触发，MAA不手动开技能。\n"
    "删除原流明所在的“奶”干员组及3技能仅开一次设置，改为固定Mon3tr槽位。"
    "原奶盾组仍保留；当前自有可用选项为塞雷娅，1技能专三、不带模组。\n"
    "原干员位置与部署顺序保留：逻各斯(9,3)左、奶盾(7,3)左、圣聆初雪(7,6)上、"
    "Mon3tr(10,5)左、乌尔比安(8,4)左；最后新增重构体(9,4)，朝上。\n"
    "重构体在Mon3tr治疗范围内，周围八格涵盖逻各斯、乌尔比安和Mon3tr，"
    "可提供攻击力增益并作为治疗链中转。其阻挡数为0，不承担阻挡任务。"
    "重构体属于召唤物，仅写部署动作，不加入自动编队干员列表。\n"
    "自有逻各斯精二60、1技能专三、Δ模组三级；圣聆初雪精二60、2技能专三、Y模组三级；"
    "乌尔比安精二60、2技能专三、X模组三级。模组三级需手动核对，MAA字段只指定模组类型。\n"
    "无需流明或助战。已核对格子、治疗范围、重构体增益范围及自有练度；未运行游戏，尚未实战验证。"
    "Mon3tr1技能提供治疗而非流明3技能的解除异常状态效果，不能视为机制完全等价替换。"
)

ids = {"逻各斯": "char_4133_logos", "圣聆初雪": "char_1046_sbell2",
       "乌尔比安": "char_4145_ulpia", "Mon3tr": "char_4179_monstr", "塞雷娅": "char_202_demkni"}
module_types = {"逻各斯": (4, "D"), "圣聆初雪": (2, "Y"), "乌尔比安": (1, "X"),
                "Mon3tr": (1, "X"), "塞雷娅": (0, None)}
for oper in job["opers"]:
    oper["requirements"] = {"elite": 2, "level": 60, "skill_level": 10,
                            "module": module_types[oper["name"]][0]}
job["opers"].append({"name": "Mon3tr", "role": "medic", "skill": 1, "skill_usage": 0,
                     "requirements": {"elite": 2, "level": 60, "skill_level": 10, "module": 1}})
job["groups"] = [g for g in job["groups"] if g["name"] != "奶"]
assert len(job["groups"]) == 1 and job["groups"][0]["name"] == "奶盾"
saria = next(o for o in job["groups"][0]["opers"] if o["name"] == "塞雷娅")
saria["requirements"] = {"elite": 2, "level": 60, "skill_level": 10, "module": 0}
for action in job["actions"]:
    if action.get("name") == "奶":
        action.update(name="Mon3tr", role="medic")
job["actions"].insert(-1, {"type": "Deploy", "name": "重构体", "location": [9, 4],
                            "direction": "Up", "doc": "治疗链中转，增益逻各斯、乌尔比安和Mon3tr。"})

# Requirement checks use the current snapshot. The unchanged defender group
# has one confirmed self-owned option, Saria; alternatives are not certified.
adaptation = []
for oper in job["opers"] + [saria]:
    own = box[ids[oper["name"]]]
    req = oper["requirements"]
    assert (own["evolvePhase"], own["level"]) >= (req["elite"], req["level"])
    assert own["mainSkillLevel"] == 7
    assert 7 + own["skills"][oper["skill"] - 1]["level"] >= req["skill_level"]
    module = module_types[oper["name"]][1]
    if module:
        assert any(e["type"] == module and e["level"] == 3 for e in own["equips"])
    adaptation.append({"name": oper["name"], "snapshot": own, "requirements": req,
                       "status": "owned_requirements_met"})

original_deploys = [a for a in original["actions"] if a["type"] == "Deploy"]
deploys = [a for a in job["actions"] if a["type"] == "Deploy"]
assert len(original_deploys) == 5 and len(deploys) == 6
for old, new in zip(original_deploys, deploys[:5]):
    assert (old["location"], old["direction"]) == (new["location"], new["direction"])
    assert new["name"] == ("Mon3tr" if old["name"] == "奶" else old["name"])
placed = set()
for action in deploys:
    x, y = action["location"]
    name = action["name"]
    assert (x, y) not in placed
    placed.add((x, y))
    assert 0 <= x < 13 and 0 <= y < 9
    is_ground = name in ["奶盾", "乌尔比安", "重构体"]
    assert mapdata["tiles"][y][x]["buildableType"] in ([1, 3] if is_ground else [2, 3])

# Range offsets describe a unit facing right; rotate by 180 degrees for Left.
mon_range = {(10 - g["col"], 5 + g["row"]) for g in ranges["y-2"]["grids"]}
assert (9, 4) in mon_range
token_range = {(9 + g["col"], 4 - g["row"]) for g in ranges["x-4"]["grids"]}
assert all(p in token_range for p in [(9, 3), (8, 4), (10, 5)])
assert skills["skchr_monstr_1"]["levels"][-1]["skillType"] == "AUTO"
assert chars["token_10050_monstr_prosts"]["phases"][2]["attributesKeyFrames"][0]["data"]["blockCnt"] == 0
assert len(deploys) <= stage["options"]["characterLimit"] == 8
assert all(o["name"] not in ["流明", "重构体"] for o in job["opers"])
assert all(a.get("name") != "奶" for a in job["actions"])
assert job["actions"][-1]["type"] == "SkillDaemon"

save("CV-8-Mon3tr-S1.json", job)
save("adaptation.json", {"snapshot": "operators-2026-11-14.json", "operators": adaptation,
                         "selected_defender": "塞雷娅", "borrow_count": 0, "combat_verified": False})
save("validation.json", {"stage": "act28side_08", "json_and_roster_checks": True,
    "original_five_positions_directions_and_order_preserved": True,
    "legal_distinct_deployment_tiles": True, "mon3tr_location": [10, 5], "mon3tr_direction": "Left",
    "mon3tr_skill": 1, "skill_triggers_in_game": True,
    "mon3tr_range_maa": sorted(mon_range), "reconstruction_location": [9, 4],
    "reconstruction_in_healing_range": True, "reconstruction_aura_maa": sorted(token_range),
    "buff_targets": ["逻各斯", "乌尔比安", "Mon3tr"], "deployments": len(deploys),
    "deployment_limit": 8, "no_summon_in_formation": True, "core_loaded": False,
    "combat_verified": False, "limits": "Static roster, geometry and JSON checks only; no combat simulation."})
print("Saved CV-8-Mon3tr-S1.json; five self-owned slots, six legal deployments, original positions preserved, token geometry checked; combat not tested.")

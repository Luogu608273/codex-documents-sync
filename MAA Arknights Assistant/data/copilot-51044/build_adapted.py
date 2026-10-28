import copy
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[1]


def read(name):
    return json.loads((BASE / name).read_text(encoding="utf-8"))


def save(name, obj):
    (BASE / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


original = read("original.json")
job = copy.deepcopy(original)
owned = json.loads((ROOT / "data/operators-2026-10-20.json").read_text(encoding="utf-8"))
box = {o["id"]: o for o in owned}
chars = read("character_table.json")
ranges = read("range_table.json")
stage = read("stage.raw.json")
normal_map = read("map.json")
raid_map = read("mapf.json")
assert normal_map["tiles"] == raid_map["tiles"]

job["minimum_required"] = "v6.18.0"
job["difficulty"] = 2
job["doc"]["title"] = "GO-EX-7 突袭｜结城理补强｜个人练度适配（待实测）"
job["doc"]["details"] = (
    "基于 prts://51044 修改，原 JSON 作者：小卡拉帕鲁灰。\n"
    "本地个人修改版，未上传覆盖原作业；2026-10-20 根据一图流快照适配，尚未实战验证。\n"
    "只标记突袭难度；请在 GO-EX-7 突袭编队选择页使用。\n"
    "自有：逻各斯精二60，1技能专三，Δ模组三级；结城理精二60，3技能专三，Y模组三级；"
    "克洛丝精一55，1技能7级；塞雷娅精二1，1技能专三，不带模组。\n"
    "唯一助战：维什戴尔，精二90，3技能专三，X模组三级。推荐自动编队，缺一人借助战；"
    "关闭额外补信赖，不要用忽略练度要求代替助战核对。\n"
    "结城理在原四人部署完成后，部署于 MAA 坐标(7,4)，朝下，3技能好了就用。"
    "其替身菱形范围覆盖右侧通路及逻各斯(9,4)，三技能攻击替身可对空；"
    "攻击替身受致命伤后可切换为治疗替身。这里不强制连续点击技能切换治疗形态。\n"
    "突袭有额外的大容量物资运输艇且部分初始位置改变；保留原防空干员。"
    "保留原四人的部署顺序，结城理最后加入，避免额外费用推迟原防线成型。\n"
    "原作业要求逻各斯满级。此版将其编队门槛改为当前60级，并增加结城理补强；"
    "这是待验证的个人配置，不是已经验证的最低练度或通关保证。\n"
    "MAA v6.18.0 的 requirements 不校验模组等级；请手动确认上述三级模组及借用干员。"
    "不要额外携带干员，场上5名干员加最多3个魂灵之影按8个部署位预算。"
)

job["opers"][0]["requirements"].update(skill_level=10)
job["opers"][1]["requirements"].update(level=60, skill_level=10)
job["opers"][2]["requirements"] = {"elite": 1, "level": 55, "skill_level": 7}
job["opers"].extend([
    {"name": "塞雷娅", "skill": 1, "skill_usage": 0,
     "requirements": {"elite": 2, "level": 1, "skill_level": 10, "module": 0}},
    {"name": "结城理", "skill": 3, "skill_usage": 1,
     "requirements": {"elite": 2, "level": 60, "skill_level": 10, "module": 2}},
])
job["groups"] = []
for action in job["actions"]:
    if action.get("name") == "盾":
        action["name"] = "塞雷娅"
job["actions"].insert(-1, {
    "type": "Deploy", "name": "结城理", "location": [7, 4], "direction": "Down",
    "doc": "右路补强：3技能攻击替身兼顾地面与空中，受致命伤后可转治疗。",
})

names = {o["name"] for o in job["opers"]}
assert len(names) == len(job["opers"]) == 5
assert job["actions"][-1]["type"] == "SkillDaemon"
placed = set()
for action in job["actions"]:
    if action["type"] != "Deploy":
        continue
    assert action["name"] in names
    x, y = action["location"]
    assert (x, y) not in placed
    placed.add((x, y))
    assert 0 <= x < raid_map["width"] and 0 <= y < raid_map["height"]
    name = action["name"]
    pos = next(v["position"] for k, v in chars.items() if k.startswith("char_") and v.get("name") == name)
    allowed = raid_map["tiles"][y][x]["buildableType"]
    assert allowed in ([1, 3] if pos == "MELEE" else [2, 3]), (name, x, y, allowed)

mapping = {
    "维什戴尔": "char_1035_wisdel", "逻各斯": "char_4133_logos", "克洛丝": "char_124_kroos",
    "塞雷娅": "char_202_demkni", "结城理": "char_4217_makoto",
}
modules = {0: None, 1: "X", 2: "Y", 3: "A", 4: "D"}
adaptation = []
for oper in job["opers"]:
    name = oper["name"]
    own = box.get(mapping[name])
    if own is None:
        adaptation.append({"name": name, "status": "borrow", "requirements": oper["requirements"], "module_level_manual": 3})
        continue
    req = oper["requirements"]
    assert (own["evolvePhase"], own["level"]) >= (req["elite"], req["level"])
    skill_level = own["mainSkillLevel"]
    if own["skills"][oper["skill"] - 1]["level"]:
        skill_level = 7 + own["skills"][oper["skill"] - 1]["level"]
    assert skill_level >= req["skill_level"]
    module_type = modules.get(req.get("module"))
    if module_type:
        assert any(m["type"] == module_type and m["level"] == 3 for m in own["equips"])
    adaptation.append({"name": name, "status": "owned_requirements_met", "snapshot": own, "requirements": req})
assert sum(a["status"] == "borrow" for a in adaptation) == 1

# Game-data rows count upward; MAA coordinates count downward from the top.
def maa(point):
    return [point["col"], raid_map["height"] - 1 - point["row"]]

coverage = [[7 + g["col"], 4 - g["row"]] for g in ranges["x-1"]["grids"]]
assert [9, 4] in coverage
assert [6, 5] in coverage
assert all([7, y] in coverage for y in [2, 3, 4, 5, 6])
assert stage["options"]["characterLimit"] == 8
assert len(job["opers"]) + 3 <= 8
route_evidence = []
for i, route in enumerate(stage["routes"]):
    points = [maa(route["startPosition"])] + [maa(c["position"]) for c in route["checkpoints"] if c["type"] == "MOVE"] + [maa(route["endPosition"])]
    route_evidence.append({"index": i, "motion": route["motionMode"], "checkpoints_maa": points})

save("GO-EX-7-raid-makoto.json", job)
save("adaptation.json", {"snapshot": "operators-2026-10-20.json", "operators": adaptation,
    "borrow_count": 1, "combat_verified": False, "original_logos_level": 90,
    "adapted_logos_level": 60, "adapted_level_is_proven_minimum": False})
save("validation.json", {"json_parsed": True, "unique_operators": True, "deployment_tiles_legal": True,
    "normal_and_raid_same_tiles": True, "original_deployment_order_preserved": True,
    "self_owned_requirements_checked": True, "modules_checked_in_snapshot": True,
    "one_borrowed_operator": "维什戴尔", "deployment_limit": 8, "operators_plus_three_revenants": 8,
    "makoto_location": [7, 4], "direction": "Down", "substitute_range": coverage,
    "covers_logos": True, "routes": route_evidence, "combat_verified": False,
    "scope": "Static JSON, map, route and roster validation only; no game execution."})
print("Saved adapted job; 5 legal deployments, 4 owned operators and 1 support, static checks passed; combat not tested.")

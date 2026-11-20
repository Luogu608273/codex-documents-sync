"""Adapt 67054 with S1 Mon3tr at Haruka's original tile; static checks only."""
import copy
import hashlib
import itertools
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
normal, raid = [read(BASE / n) for n in ["map.json", "map-raid.json"]]
stage = read(BASE / "stage.raw.json")
characters = read(BASE / "character_table.json")
ranges = read(BASE / "range_table.json")
skills = read(BASE / "skill_table.json")
roster_path = ROOT / "data/operators-2026-11-19.json"
roster = {o["id"]: o for o in read(roster_path)}
assert original["stage_name"] == normal["stageId"] == "act27side_ex07"
assert normal["tiles"] == raid["tiles"]
positions = {a["name"]: tuple(a["location"]) for a in original["actions"]
             if a["type"] == "Deploy" and a["name"] not in ["遥", "水汽汽水瓶"]}
positions.update(Mon3tr=(2, 5), 重构体=(2, 4))
local = ["Mon3tr", "歌蕾蒂娅", "斩业星熊", "重构体"]
ground = ["歌蕾蒂娅", "斩业星熊"]
ranks = {"Mon3tr": 0, "歌蕾蒂娅": 1, "乌尔比安": 2, "斩业星熊": 3, "重构体": 4}


def adjacent(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1])) <= 1


def area(direction):
    result = set()
    for grid in ranges["y-2"]["grids"]:
        dx, dy = grid["col"], -grid["row"]
        if direction == "Up":
            dx, dy = dy, -dx
        elif direction == "Down":
            dx, dy = -dy, dx
        elif direction == "Left":
            dx, dy = -dx, -dy
        result.add((2 + dx, 5 + dy))
    return result


def chain(root, hp=None, coords=None, budget=4):
    """Conservative four-recipient budget; root is specified, not S2-forced.

    No healing amounts/HP updates are simulated. Skill/token extra allowances
    can lengthen a chain, but cannot bridge the disconnected right-side ally.
    """
    hp = hp or {}
    coords = coords or positions
    path = [root]
    while len(path) < budget:
        candidates = [n for n in coords if n not in path and adjacent(coords[path[-1]], coords[n])]
        if not candidates:
            break
        path.append(min(candidates, key=lambda n: (hp.get(n, 1.0), -ranks[n])))
    return path


healing_area = area("Up")
assert all(positions[n] in healing_area for n in local)
assert positions["乌尔比安"] not in healing_area
assert all(not adjacent(positions["乌尔比安"], positions[n]) for n in local)
assert chain("重构体") == ["重构体", "斩业星熊", "歌蕾蒂娅"]
assert chain("歌蕾蒂娅") == ["歌蕾蒂娅", "重构体", "斩业星熊", "Mon3tr"]
assert chain("斩业星熊") == ["斩业星熊", "重构体", "歌蕾蒂娅"]
# HP can override same-HP deployment priority and shorten coverage.
counterexample = chain("斩业星熊", {"斩业星熊": 0.2, "重构体": 0.3, "Mon3tr": 0.4})
assert counterexample == ["斩业星熊", "重构体", "Mon3tr"]

mon = next(o for o in job["opers"] if o["name"] == "遥")
mon.clear()
mon.update(name="Mon3tr", role="medic", skill=1, skill_usage=0,
           requirements={"elite": 2, "level": 60, "skill_level": 10, "module": 1})
for action in job["actions"]:
    if action.get("name") == "遥":
        action.update(name="Mon3tr", role="medic", direction="Up")
first_bottle = next(i for i, a in enumerate(job["actions"]) if a.get("name") == "水汽汽水瓶")
job["actions"].insert(first_bottle + 1, {
    "type": "Deploy", "name": "重构体", "location": [2, 4], "direction": "Up",
    "doc": "先放原第一瓶汽水，再放重构体；邻接左侧两名地面干员及Mon3tr。",
})
job["minimum_required"] = "v6.18.0"
job["doc"]["title"] = "SL-EX-7 离家五百里｜Mon3tr原位一技能与重构体（待实测）"
job["doc"]["details"] = original["doc"]["details"] + (
    "\n\n本地修改基于prts://67054，未修改线上原作业。"
    "按用户要求遥换医疗Mon3tr，保留遥原位MAA(2,5)，朝向调整为上。"
    "配置精二60、一技能专三、X模组三级；一技能由游戏自动触发，skill_usage=0不禁止自动技能，"
    "无需MAA手动开技，也不添加SkillUsage动作。\n"
    "重构体放(2,4)朝上，插入原第一瓶水汽汽水瓶(3,3)之后、15杀的第二瓶之前。"
    "其余三名干员的技能、位置、朝向和相对顺序均保留；三次汽水瓶的位置、方向与15/24杀条件保留。"
    "重构体不加入自动编队名单。\n"
    "Mon3tr朝上可直接治疗歌蕾蒂娅(2,3)、斩业星熊(3,4)、重构体(2,4)及自身。"
    "重构体周围八格同时覆盖左侧两名地面干员和Mon3tr，提供增益并参与治疗跳跃。"
    "右侧乌尔比安(9,1)与左侧断开，本版本不保证治疗乌尔比安。\n"
    "跳跃优先低生命比例，同血比优先后部署者；一条链不重复选取已经治疗的目标。"
    "保留Mon3tr→歌蕾蒂娅→乌尔比安→斩业星熊的干员部署顺序，再追加重构体。"
    "以重构体起链且后续候选同血比时：重构体→斩业星熊→歌蕾蒂娅，优先覆盖左侧地面。"
    "以歌蕾蒂娅起链且其余同血比时：歌蕾蒂娅→重构体→斩业星熊→Mon3tr。"
    "一技能不会像二技能一样固定优先以重构体起链；起点取决于治疗目标。"
    "若Mon3tr伤得比歌蕾蒂娅更重，链可能提前转向自身而漏掉歌蕾蒂娅；不能保证每条链覆盖全部左侧单位。"
    "不额外部署其他干员或改变顺序。\n"
    "一技能额外跳跃与重构体额外不衰减跳跃均不等于每次必定奶满四人；容量充足仍会因末端无可选目标断链。"
    "水汽汽水瓶属于敌方装置，不作为友方治疗跳板。保留原三瓶汽水用于关卡水汽机制。\n"
    "练度依据2026-11-19一图流快照：Mon3tr符合上述配置；未在本次刷新一图流。"
    "斩业星熊未持有，仍需按原作业准备/借用其一技能。歌蕾蒂娅自有一技能7级，原作业未写最低专精要求。"
    "Mon3tr费用高于遥，后续部署到场时间可能变化；治疗替换还会失去遥的原有攻击与支援效果。"
    "仅完成JSON、普通/突袭合法地块、部署容量、技能类型及静态链路检查，未实战验证。"
)

own = roster["char_4179_monstr"]
assert own["evolvePhase"] == 2 and own["level"] >= 60 and own["mainSkillLevel"] == 7
assert next(s for s in own["skills"] if s["id"] == "skchr_monstr_1")["level"] == 3
assert any(e["type"] == "X" and e["level"] == 3 for e in own["equips"])
assert skills["skchr_monstr_1"]["levels"][-1]["skillType"] == "AUTO"
assert "char_1044_hsgma2" not in roster
deploys = [a for a in job["actions"] if a["type"] == "Deploy" and a["name"] != "水汽汽水瓶"]
assert len(deploys) == len({tuple(a["location"]) for a in deploys}) == 5
predefined_tiles = {(t["position"]["col"], t["position"]["row"])
                    for t in stage["predefines"]["tokenInsts"]}
bottles = [a for a in original["actions"] if a.get("name") == "水汽汽水瓶"]
for a in deploys:
    x, y = a["location"]
    expected = 2 if a["name"] == "Mon3tr" else 1
    for m in [normal, raid]:
        assert m["tiles"][y][x]["buildableType"] == expected
    assert (x, y) not in predefined_tiles
    assert all([x, y] != b["location"] for b in bottles)
assert next(a for a in deploys if a["name"] == "Mon3tr")["location"] == next(
    a for a in original["actions"] if a.get("name") == "遥")["location"]
assert [a for a in job["actions"] if a.get("name") == "水汽汽水瓶"] == bottles
assert all(a in job["actions"] for a in original["actions"] if a.get("name") not in ["遥"])
assert all(o in job["opers"] for o in original["opers"] if o["name"] != "遥")
assert all(o["name"] not in ["遥", "重构体"] for o in job["opers"])
assert not any(a["type"] in ["Skill", "SkillUsage"] and a.get("name") == "Mon3tr" for a in job["actions"])
assert len(deploys) + 1 <= stage["options"]["characterLimit"] == 8  # conservative extra slot for bottle
assert job["difficulty"] == original["difficulty"] == 3

scenarios = []
for ratios in itertools.product([0.3, 0.6, 1.0], repeat=4):
    hp = dict(zip(local, ratios))
    for root in local:
        path = chain(root, hp)
        scenarios.append({"root": root, "hp": hp, "path": path,
                          "ground_recipients": [n for n in ground if n in path]})
save("SL-EX-7-Mon3tr-S1.json", job)
save("validation.json", {
    "stage": job["stage_name"], "difficulty": 3, "Mon3tr_original_tile_preserved": True,
    "Mon3tr": [2, 5, "Up"], "reconstruction": [2, 4, "Up"],
    "skill": 1, "game_auto_trigger": True, "legal_normal_and_raid_tiles": True,
    "original_other_operators_and_bottles_preserved": True,
    "direct_healing_area": sorted(healing_area), "token_aura_all_three_left_allies": True,
    "token_root_equal_HP": chain("重构体"), "gladiia_root_equal_HP": chain("歌蕾蒂娅"),
    "HP_counterexample": counterexample, "per_chain_joint_ground_coverage_guaranteed": False,
    "right_side_ulpianus_unreachable": True,
    "scenario_count": len(scenarios), "scenarios": scenarios,
    "scenario_scope": "Four specified roots x 81 fixed HP states; conservative four-recipient capacity. Not a primary-target/HP-update/combat simulation.",
    "roster_snapshot": roster_path.name, "owned_Mon3tr_requirements_met": True,
    "support_needed": "斩业星熊 S1", "combat_verified": False,
})
save("roster-reference.json", {"snapshot": roster_path.name,
    "snapshot_sha256": hashlib.sha256(roster_path.read_bytes()).hexdigest(),
    "Mon3tr": own, "refreshed_this_task": False})
print("Saved SL-EX-7-Mon3tr-S1.json; original tile and bottle actions preserved; 324 static chain cases; combat not tested.")

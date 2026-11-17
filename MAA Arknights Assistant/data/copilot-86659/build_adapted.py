"""Add Mon3tr S1 to BB-EX-6 and check static rope and healing geometry."""
import copy
import json
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[1]


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def save(name, value):
    (BASE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


original = read(BASE / "original.json")
job = copy.deepcopy(original)
mapdata = read(BASE / "map.json")
stage = read(BASE / "stage.raw.json")
ranges = read(BASE / "range_table.extract.json")
skills = read(BASE / "skill_table.extract.json")
box = {o["id"]: o for o in read(ROOT / "data/operators-2026-11-17.json")}
assert original["stage_name"] == mapdata["stageId"] == "act33side_ex06"
job["minimum_required"] = "v6.18.0"
job["doc"]["title"] = "BB-EX-6 越过障碍｜追加Mon3tr一技能（待实测）"
job["doc"]["details"] = (
    original["doc"]["details"]
    + "\n\n本地修改版，基于prts://86659，未覆盖线上作业。\n"
    "新增Mon3tr：精二60、1技能专三、X模组三级，部署于MAA坐标(10,5)，朝上。"
    "1技能由游戏自动触发，MAA不手动点击。其直接治疗范围包含歌蕾蒂娅(10,3)与乌尔比安(9,4)，"
    "逻各斯(10,2)由治疗链跳跃支援，不属于此朝向下的直接治疗范围。\n"
    "保留原顺序与位置：先歌蕾蒂娅(10,3)左，再乌尔比安(9,4)上，再逻各斯(10,2)下，"
    "加速后部署Mon3tr，最后挂机。本版不额外部署重构体或其他干员。\n"
    "铁链：乌尔比安处于接驳地块，先连接歌蕾蒂娅；逻各斯随后从普通高台连接乌尔比安，"
    "使其达到两条铁链上限。Mon3tr最后落在普通高台tile_wall，不依赖锁链部署；"
    "此前的两条连接不因她落地而改选。不可提前部署Mon3tr或随意撤走原铁链端点。\n"
    "普通/突袭标记沿用原作业；Mon3tr位置不在突袭封锁的8个格子中。\n"
    "2026-11-17一图流复核：Mon3tr配置达标；歌蕾蒂娅自有1技能仅7级，"
    "低于原作业专三要求。该要求保持原值，请将其练到专三或借用精二60、1技能专三、X三级模组的歌蕾蒂娅。"
    "原作业其他干员技能和模组要求保持。MAA不校验模组等级，需手动确认。\n"
    "已检查地块、直接治疗范围、原部署顺序、铁链容量与静态连接选择；没有连接游戏或实战，不能视为已通关。"
)
job["opers"].append({"name": "Mon3tr", "role": "medic", "skill": 1, "skill_usage": 0,
                     "requirements": {"elite": 2, "level": 60, "skill_level": 10, "module": 1}})
job["actions"].append({"type": "Deploy", "name": "Mon3tr", "role": "medic",
                       "location": [10, 5], "direction": "Up",
                       "doc": "原两条锁链建立后，普通高台补奶；1技能自动触发。"})
job["actions"].append({"type": "SkillDaemon"})
assert job["opers"][:-1] == original["opers"]
assert job["actions"][:-2] == original["actions"]
assert job["difficulty"] == original["difficulty"] == 3

ids = {"歌蕾蒂娅": "char_474_glady", "乌尔比安": "char_4145_ulpia",
       "逻各斯": "char_4133_logos", "Mon3tr": "char_4179_monstr"}
modules = {1: "X", 4: "D"}
adaptation = []
for oper in job["opers"]:
    own = box[ids[oper["name"]]]
    req = oper["requirements"]
    actual_skill = own["mainSkillLevel"]
    mastery = own["skills"][oper["skill"] - 1]["level"]
    if mastery:
        actual_skill = 7 + mastery
    module_level = max(e["level"] for e in own["equips"] if e["type"] == modules[req["module"]])
    reasons = []
    if actual_skill < req["skill_level"]:
        reasons.append("skill_level")
    if module_level < 3:
        reasons.append("module_level_manual")
    adaptation.append({"name": oper["name"], "snapshot": own,
                       "actual_skill_level": actual_skill, "module_level": module_level,
                       "original_requirements_preserved": oper["name"] != "Mon3tr",
                       "shortfalls": reasons, "requirements": req})
assert [o["name"] for o in adaptation if o["shortfalls"]] == ["歌蕾蒂娅"]

rope_tiles = {"tile_merope", "tile_rarope"}
support_offsets = {(g["col"], -g["row"]) for g in ranges["x-2"]["grids"]}
# Verify this support shape against the PRTS mechanism's rendered HTML grid.
html = (BASE / "babel-mechanics.html").read_text(encoding="utf-8")
section = html[html.index("支援范围："):][:6500]
rows = re.findall(r'<div style="height:22px;">(.*?)</div></div>', section)[:5]
wiki_offsets = set()
for y, row in enumerate(rows):
    cells = re.findall(r'<div style="([^"]*)"', row)
    assert len(cells) == 5
    for x, style in enumerate(cells):
        if "border:" in style or "background-color:" in style:
            wiki_offsets.add((x - 2, y - 2))
assert wiki_offsets == support_offsets

raid_forbidden = set()
for rune in stage["runes"]:
    if rune["key"] == "global_forbid_location":
        for entry in rune["blackboard"]:
            for row, col in re.findall(r"\((\d+),(\d+)\)", entry["valueStr"] or ""):
                raid_forbidden.add((int(col), mapdata["height"] - 1 - int(row)))
assert len(raid_forbidden) == 8
assert all(y in [1, 6] and x in range(6, 10) for x, y in raid_forbidden)

deployed = []
edges = []
counts = {}
events = []
for action in job["actions"]:
    if action["type"] != "Deploy":
        continue
    name = action["name"]
    x, y = action["location"]
    point = (x, y)
    assert point not in raid_forbidden
    assert point not in [d["point"] for d in deployed]
    tile = mapdata["tiles"][y][x]
    assert tile["buildableType"] == (1 if name in ["乌尔比安", "歌蕾蒂娅"] else 2)
    on_rope = tile["tileKey"] in rope_tiles
    candidates = [d for d in deployed
                  if (d["point"][0] - x, d["point"][1] - y) in support_offsets
                  and counts[d["name"]] < 2 and (on_rope or d["on_rope"])]
    counts[name] = 0
    if on_rope:
        assert candidates, "Connecting tile requires a valid earlier rope endpoint"
    if candidates:
        target = candidates[-1]
        edges.append([target["name"], name])
        counts[name] += 1
        counts[target["name"]] += 1
    events.append({"name": name, "location": point, "tile": tile["tileKey"],
                   "new_edge": edges[-1] if candidates else None, "rope_counts": dict(counts)})
    deployed.append({"name": name, "point": point, "on_rope": on_rope})
assert edges == [["歌蕾蒂娅", "乌尔比安"], ["乌尔比安", "逻各斯"]]
assert counts == {"歌蕾蒂娅": 1, "乌尔比安": 2, "逻各斯": 1, "Mon3tr": 0}
assert max(counts.values()) <= 2

# Right-facing offsets: forward=col, left=row. Up rotates forward to negative y.
healing = {(10 - g["row"], 5 - g["col"]) for g in ranges["y-2"]["grids"]}
assert (10, 3) in healing and (9, 4) in healing
assert (10, 2) not in healing
assert abs(10 - 10) <= 1 and abs(3 - 2) <= 1  # Adjacent Gladiia -> Logos jump.
assert skills["skchr_monstr_1"]["levels"][-1]["skillType"] == "AUTO"
assert len(deployed) == 4 <= stage["options"]["characterLimit"]
save("BB-EX-6-Mon3tr-S1.json", job)
save("adaptation.json", {"roster_date": "2026-11-17", "operators": adaptation,
                         "support_recommended": "歌蕾蒂娅", "combat_verified": False})
save("validation.json", {"stage": original["stage_name"], "original_operators_and_actions_preserved": True,
    "difficulty": job["difficulty"], "mon3tr_location": [10, 5], "direction": "Up",
    "normal_tile": "tile_wall", "raid_blocked_tiles": sorted(raid_forbidden),
    "mon3tr_direct_healing_range": sorted(healing), "direct_targets": ["歌蕾蒂娅", "乌尔比安"],
    "logos_needs_chain_jump": True, "rope_support_offsets": sorted(support_offsets),
    "rope_events": events, "rope_edges": edges, "rope_counts": counts,
    "deployments": 4, "deploy_limit": stage["options"]["characterLimit"],
    "reconstruction_deployed": False, "core_loaded": False, "combat_verified": False,
    "limits": "Static connection model assumes all original units remain on field; it does not validate survival or healing-chain target priority."})
print("Saved BB-EX-6-Mon3tr-S1.json; Mon3tr (10,5) Up, original rope edges preserved; Gladiia S1 mastery shortfall remains; combat not tested.")

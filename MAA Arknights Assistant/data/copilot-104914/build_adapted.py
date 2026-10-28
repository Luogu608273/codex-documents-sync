"""Build and statically check a local TW-EX-7 adaptation; never controls the game."""
import copy
import hashlib
import json
from collections import deque
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[1]


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def save(name, value):
    (BASE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


original = load(BASE / "original.json")
job = copy.deepcopy(original)
box = {o["id"]: o for o in load(ROOT / "data/operators-2026-10-23.json")}
chars = load(BASE / "character_table.json")
skills = load(BASE / "skill_table.json")
ranges = load(BASE / "range_table.json")
mapdata = load(BASE / "map.json")
raidmap = load(BASE / "map-raid.json")
stage = load(BASE / "stage.raw.json")
assert original["stage_name"] == "act11d0_ex07"
assert mapdata["tiles"] == raidmap["tiles"]

job["minimum_required"] = "v6.18.0"
job["doc"]["title"] = "TW-EX-7 分别计算｜凛御银灰＋塞雷娅补强（待实测）"
job["doc"]["details"] = (
    "基于 prts://104914 的本地个人修改版，原作业为“分别计算挂机”。保留普通/突袭标记，均未实战验证。\n"
    "自有：圣聆初雪精二60、2技能专三、Y模组三级；结城理精二60、3技能专三、Y模组三级；"
    "Lancet-2精零1级，仅编队，不部署。唯一助战：凛御银灰精二90、3技能专三，无模组要求。\n"
    "新增自有塞雷娅：精二60、2技能7级、不使用模组；上一版用户反馈突袭未通过，本版待实测。\n"
    "自动编队需借用凛御银灰；不要额外补信赖、不要额外加人，避免首次技能费用交换与协同攻击选错目标。\n"
    "保留前三个障碍物操作；随后凛御银灰部署在MAA坐标(7,3)，朝右，先显式开一次3技能，"
    "再设为好了就用。首次开技时，圣聆初雪与Lancet-2仍在待部署区，交换24费与3费；"
    "随后先部署圣聆初雪，接收这次技能的协同攻击。小车始终不部署。\n"
    "凛御银灰避开障碍物引导后的主要行进通路，技能覆盖右侧(10,3)及临时改道区(8,4)/(9,4)；"
    "在场时还给圣聆初雪提供谢拉格干员的自愈、加防与免冻。\n"
    "原作业前三箱的费用条件保留；开凛御银灰技能后的三处费用增长等待改为二倍速下2500/1500/2500毫秒延时，"
    "近似保留原来5/3/5游戏秒的等待，避免新增回费提前触发撤箱。保持全程二倍速。\n"
    "保留结城理原单次手动开技、不改为循环；圣聆初雪2技能由游戏自动开启，MAA不反复点击关闭。"
    "撤除(10,5)障碍物后，仍补箱到(8,6)，再部署塞雷娅于(8,4)，朝上，随后挂机。"
    "塞雷娅2技能由游戏自动治疗，范围覆盖初雪(8,2)及凛御银灰(7,3)，不覆盖结城理(10,2)。"
    "不要将塞雷娅改为3技能或挪动结城理；其3技能会覆盖到结城理。\n"
    "两名自有核心原要求90级，本版改为当前60级并增加补强；这不是已验证的最低练度。"
    "模组等级需手动核对，MAA requirements仅指定模组类型。当前只做静态校验，未连接游戏、未测试通关。"
)

for oper in job["opers"]:
    oper["requirements"]["level"] = 60
    oper["skill_usage"] = 0
job["opers"].extend([
    {"name": "凛御银灰", "skill": 3, "skill_usage": 0,
     "requirements": {"elite": 2, "level": 90, "skill_level": 10, "module": 0}},
    {"name": "Lancet-2", "skill": 0, "skill_usage": 0,
     "requirements": {"elite": 0, "level": 1}},
    {"name": "塞雷娅", "skill": 2, "skill_usage": 0,
     "requirements": {"elite": 2, "level": 60, "skill_level": 7, "module": 0}},
])

# Disable auto skill until the first explicit activation so it cannot fire while
# the following explicit Skill action is still waiting for the same first cast.
job["actions"][4:4] = [
    {"type": "Deploy", "name": "凛御银灰", "location": [7, 3], "direction": "Right",
     "doc": "先下凛御银灰；Lancet-2与圣聆初雪留在待部署区。"},
    {"type": "Skill", "name": "凛御银灰",
     "doc": "首次3技能：初雪与小车交换费用，下一位部署初雪获得协同攻击。"},
    {"type": "SkillUsage", "name": "凛御银灰", "skill_usage": 1,
     "doc": "凛御银灰此后3技能好了就开。"},
]

delay_changes = []
for action in job["actions"]:
    if action.get("cost_changes") == 5 or (action["type"] == "BulletTime" and action.get("cost_changes") == 3):
        old = action.pop("cost_changes")
        delay = old * 500  # One real second is two game seconds at 2x speed.
        action["pre_delay"] = delay
        delay_changes.append({"type": action["type"], "name": action.get("name"),
                              "location": action.get("location"), "original_cost_changes": old,
                              "new_pre_delay_ms": delay})
assert len(delay_changes) == 3
job["actions"].insert(-1, {
    "type": "Deploy", "name": "塞雷娅", "location": [8, 4], "direction": "Up",
    "doc": "换箱完成后补奶：2技能覆盖初雪与凛御银灰，不覆盖结城理。",
})

ids = {"圣聆初雪": "char_1046_sbell2", "结城理": "char_4217_makoto",
       "凛御银灰": "char_1045_svash2", "Lancet-2": "char_285_medic2", "塞雷娅": "char_202_demkni"}
adaptation = []
for oper in job["opers"]:
    own = box.get(ids[oper["name"]])
    req = oper["requirements"]
    if own is None:
        assert oper["name"] == "凛御银灰"
        adaptation.append({"name": oper["name"], "status": "borrow", "requirements": req})
        continue
    assert (own["evolvePhase"], own["level"]) >= (req["elite"], req["level"])
    if oper["skill"]:
        skill_level = own["mainSkillLevel"]
        mastery = own["skills"][oper["skill"] - 1]["level"]
        if mastery:
            skill_level = 7 + mastery
        assert skill_level >= req["skill_level"]
    if req.get("module") == 2:
        assert any(e["type"] == "Y" and e["level"] == 3 for e in own["equips"])
    adaptation.append({"name": oper["name"], "status": "owned_requirements_met",
                       "snapshot": own, "requirements": req})

positions = {}
crates = set()
crate_actions_original = [(a["type"], a.get("location")) for a in original["actions"]
                          if a.get("name") == "障碍物" or a["type"] == "Retreat"]
crate_actions_adapted = [(a["type"], a.get("location")) for a in job["actions"]
                         if a.get("name") == "障碍物" or a["type"] == "Retreat"]
assert crate_actions_original == crate_actions_adapted
for action in job["actions"]:
    if action["type"] == "Deploy":
        x, y = action["location"]
        assert 0 <= x < 12 and 0 <= y < 9
        assert action["direction"] in ["Right", "Left", "Up", "Down", "None"]
        assert (x, y) not in crates and (x, y) not in positions.values()
        if action["name"] == "障碍物":
            assert mapdata["tiles"][y][x]["buildableType"] in [1, 3]
            crates.add((x, y))
        else:
            assert action["name"] in ids
            pos = chars[ids[action["name"]]]["position"]
            allowed = [1, 3] if pos == "MELEE" else [2, 3]
            assert mapdata["tiles"][y][x]["buildableType"] in allowed
            positions[action["name"]] = (x, y)
    elif action["type"] == "Retreat":
        crates.remove(tuple(action["location"]))
assert positions == {"凛御银灰": (7, 3), "圣聆初雪": (8, 2), "结城理": (10, 2), "塞雷娅": (8, 4)}
assert crates == {(1, 3), (5, 3), (7, 4), (8, 6)}
assert all(a.get("name") != "Lancet-2" for a in job["actions"])
assert sum(o["status"] == "borrow" for o in adaptation) == 1
assert job["difficulty"] == original["difficulty"] == 3

svash_skill = skills["skchr_svash2_3"]["levels"][-1]
assert svash_skill["spData"]["initSp"] == 46 and svash_skill["spData"]["spCost"] == 55
assert chars["char_1046_sbell2"]["phases"][2]["attributesKeyFrames"][0]["data"]["cost"] == 24
assert chars["char_285_medic2"]["phases"][0]["attributesKeyFrames"][0]["data"]["cost"] == 3
assert chars["char_202_demkni"]["phases"][2]["attributesKeyFrames"][0]["data"]["cost"] == 22
coverage = [[7 + g["col"], 3 - g["row"]] for g in ranges[svash_skill["rangeId"]]["grids"]]
assert [10, 3] in coverage and [8, 4] in coverage and [9, 4] in coverage
saria_skill = skills["skchr_demkni_2"]["levels"][6]
assert saria_skill["skillType"] == "AUTO"
saria_coverage = [[8 + g["col"], 4 - g["row"]] for g in ranges[saria_skill["rangeId"]]["grids"]]
assert [8, 2] in saria_coverage and [7, 3] in saria_coverage
assert [10, 2] not in saria_coverage
# The 3-skill range would include Makoto; explicitly lock this job to skill 2.
assert next(o for o in job["opers"] if o["name"] == "塞雷娅")["skill"] == 2

# The map array is already top-to-bottom. Entity route positions instead use
# bottom-origin row coordinates; do not reverse the map array a second time.
rawmap = stage["mapData"]
assert all(rawmap["tiles"][rawmap["map"][y][x]]["tileKey"] == mapdata["tiles"][y][x]["tileKey"]
           for y in range(9) for x in range(12))
walk = {(x, y) for y in range(9) for x in range(12)
        if rawmap["tiles"][rawmap["map"][y][x]]["passableMask"] == "ALL"}


def grid_path(start, blocked):
    queue = deque([start])
    prev = {start: None}
    while queue:
        cur = queue.popleft()
        if cur == (0, 2):
            path = []
            while cur is not None:
                path.append(list(cur))
                cur = prev[cur]
            return path[::-1]
        for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            nxt = cur[0] + dx, cur[1] + dy
            if nxt in walk and nxt not in blocked and nxt not in prev:
                prev[nxt] = cur
                queue.append(nxt)
    raise AssertionError("Crates block every route")


paths = []
for blocked in [{(1, 3), (5, 3), (7, 4), (10, 5)}, crates]:
    for start in [(0, 7), (11, 7)]:
        path = grid_path(start, blocked)
        assert [7, 3] not in path
        if blocked == crates:
            assert [8, 4] not in path
        paths.append({"start": start, "crates": sorted(blocked), "path": path})

save("TW-EX-7-silverash-robot.json", job)
save("adaptation.json", {"retrieval_date": "2026-10-23", "operators": adaptation,
                         "robot_stays_in_hand": True, "original_core_levels": [90, 90],
                         "adapted_core_levels": [60, 60], "previous_version_raid_result": "user_reported_failure",
                         "saria_does_not_heal_makoto": True, "combat_verified": False})
save("validation.json", {"stage": job["stage_name"], "difficulty": job["difficulty"],
    "json_and_deployment_checks_passed": True, "borrow_count": 1,
    "crate_locations_and_order_preserved": True, "final_crates": sorted(crates),
    "first_svash_skill_is_explicit_then_auto": True, "robot_not_deployed": True,
    "first_swap_expected": {"圣聆初雪": [24, 3], "Lancet-2": [3, 24]},
    "initial_sp_without_other_buffs": 50, "first_cast_wait_game_seconds_without_other_buffs": 5,
    "svash_skill_range_maa": coverage, "wait_changes": delay_changes,
    "saria": {"location": [8, 4], "direction": "Up", "skill": 2, "skill_level": 7,
              "heal_range_maa": saria_coverage, "heals_sbell2": True, "heals_svash2": True,
              "heals_makoto": False, "deploy_after_final_crate": True,
              "base_cost_22_below_sbell2_24": True},
    "static_four_neighbor_paths": paths,
    "path_check_limit": "Grid reachability and sample shortest paths only; not a game pathfinding or combat simulation.",
    "core_loaded": False, "combat_verified": False,
    "source_job_sha256": hashlib.sha256((BASE / "original.json").read_bytes()).hexdigest()})
print("Saved TW-EX-7-silverash-robot.json; roster, deployment, crate order, skill configuration and static path checks passed; combat not tested.")

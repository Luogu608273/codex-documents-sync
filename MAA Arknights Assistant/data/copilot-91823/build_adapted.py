"""Build 91823 with original-tile S1 Mon3tr and early reconstruction."""
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
mapdata, raid = [read(BASE / n) for n in ["map.json", "map-raid.json"]]
stage = read(BASE / "stage.raw.json")
ranges = read(BASE / "range_table.json")
skills = read(BASE / "skill_table.json")
assert original["stage_name"] == mapdata["stageId"] == "act27side_ex07"
assert mapdata["tiles"] == raid["tiles"]
positions = {a["name"]: tuple(a["location"]) for a in original["actions"]
             if a["type"] == "Deploy" and a["name"] not in ["遥", "水汽汽水瓶"]}
positions.update(Mon3tr=(2, 2), 重构体=(1, 3))
local = ["凛御银灰", "圣聆初雪", "歌蕾蒂娅", "Mon3tr", "斩业星熊", "重构体"]
ground = ["凛御银灰", "歌蕾蒂娅", "斩业星熊"]
area = {(2 - (-g["row"]), 2 + g["col"]) for g in ranges["y-2"]["grids"]}
assert all(positions[n] in area for n in local)
bottles = [a for a in original["actions"] if a.get("name") == "水汽汽水瓶"]
occupied = {tuple(a["location"]) for a in original["actions"] if a["type"] == "Deploy"}
legal_tokens = sorted((x, y) for x, y in area if 0 <= x < mapdata["width"] and 0 <= y < mapdata["height"]
                      and mapdata["tiles"][y][x]["buildableType"] == 1 and (x, y) not in occupied)
assert legal_tokens == [(1, 3)]  # bottle tile remains reserved


def adjacent(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1])) <= 1


def ranks_for(actions):
    return {a["name"]: i for i, a in enumerate(a for a in actions
            if a["type"] == "Deploy" and a["name"] != "水汽汽水瓶")}


def chain(root, ranks, hp=None, enhanced=True):
    """S1: four normal recipients; ordinary heal: three; token adds one.

    Input fixes the primary recipient. This does not force S1 to choose the
    token or simulate healing amounts, HP updates, target loss, or combat.
    """
    hp = hp or {}
    path = [root]
    budget = (4 if enhanced else 3) + (root == "重构体")
    while len(path) < budget:
        choices = [n for n in positions if n not in path and adjacent(positions[path[-1]], positions[n])]
        if not choices:
            break
        target = min(choices, key=lambda n: (hp.get(n, 1.0), -ranks[n]))
        path.append(target)
        if target == "重构体":
            budget += 1
    return path


mon = next(o for o in job["opers"] if o["name"] == "遥")
mon.clear()
mon.update(name="Mon3tr", role="medic", skill=1, skill_usage=0,
           requirements={"elite": 2, "level": 60, "skill_level": 10, "module": 1})
for a in job["actions"]:
    if a.get("name") == "遥":
        a.update(name="Mon3tr", role="medic")
mon_index = next(i for i, a in enumerate(job["actions"]) if a.get("name") == "Mon3tr")
token_action = {"type": "Deploy", "name": "重构体", "location": [1, 3], "direction": "Up",
                "doc": "Mon3tr落地后立即部署；利用持续失血尽可能以重构体起链，不等待其他干员和汽水瓶。"}
# Compare feasible insertion times while keeping all original actions ordered.
timings = []
for index in range(mon_index + 1, len(job["actions"])):
    candidate = job["actions"][:index] + [token_action] + job["actions"][index:]
    r = ranks_for(candidate)
    enhanced_paths = {n: chain(n, r) for n in local}
    ordinary_paths = {n: chain(n, r, enhanced=False) for n in local}
    score = (sum(g in enhanced_paths["重构体"] for g in ground),
             sum(all(g in path for g in ground) for path in enhanced_paths.values()),
             sum(g in path for path in enhanced_paths.values() for g in ground),
             sum(g in path for path in ordinary_paths.values() for g in ground), -index)
    timings.append({"insert_index": index, "score": score, "enhanced_paths": enhanced_paths,
                    "ordinary_paths": ordinary_paths})
timings.sort(key=lambda c: c["score"], reverse=True)
assert timings[0]["insert_index"] == mon_index + 1
job["actions"].insert(mon_index + 1, token_action)
ranks = ranks_for(job["actions"])
assert chain("重构体", ranks) == ["重构体", "Mon3tr", "歌蕾蒂娅", "斩业星熊", "凛御银灰"]
assert chain("重构体", ranks, enhanced=False) == ["重构体", "Mon3tr", "歌蕾蒂娅", "斩业星熊"]
assert all(not adjacent(positions["乌尔比安"], positions[n]) for n in local)
assert positions["乌尔比安"] not in area
job["minimum_required"] = "v6.18.0"
job["doc"]["title"] = "SL-EX-7 离家五百里｜91823 Mon3tr原位一技能与重构体（待实测）"
job["doc"]["details"] = original["doc"]["details"] + (
    "\n\n本地修改基于prts://91823，未修改线上原作业。"
    "遥换为医疗Mon3tr，保留原位(2,2)朝下；精二60、一技能专三、X模组三级，MAA模组类型1。"
    "一技能由游戏自动触发，skill_usage=0表示无需MAA点击；已移除遥原来的限两次开技设置。\n"
    "Mon3tr落地后立即在(1,3)朝上部署重构体，再继续原乌尔比安、斩业星熊与水汽汽水瓶动作。"
    "利用重构体持续失血尽可能让其成为治疗起点；一技能仍会优先选择血比更低的友方，不能固定强制先奶重构体。"
    "在保留原其他部署位置、动作顺序、汽水瓶(3,3)占位且重构体位于直接治疗范围内的条件下，(1,3)是唯一空闲地面位置。\n"
    "Mon3tr直接范围覆盖左侧五名干员及重构体；重构体周围八格覆盖初雪、Mon3tr、歌蕾蒂娅、凛御银灰，未覆盖斩业星熊。"
    "以重构体起链、后续候选同血比且一技能强化治疗时：重构体→Mon3tr→歌蕾蒂娅→斩业星熊→凛御银灰。"
    "这五个治疗落点包含天赋额外不衰减的重构体，四个普通目标为Mon3tr和三名地面干员。"
    "未触发一技能的普通治疗，同条件会在斩业星熊处耗尽目标数，不能保证继续到凛御银灰。\n"
    "跳跃按最低生命比例优先，同血比按最后部署优先，一条链不重复治疗已经经过的目标。"
    "低血比会改变路径；不能保证每条链都以重构体起始或覆盖三名地面干员及初雪。"
    "重构体提前部署可减少其他起点的治疗过早被其吸引；不要额外部署单位或随意改顺序。"
    "右侧乌尔比安(9,1)与左侧链路断开，本版不保证治疗他。\n"
    "其余五名干员的技能、要求、位置、朝向和相对部署顺序全部保留。汽水瓶(3,3)及车组保留，车组原本没有部署动作，继续不部署。"
    "召唤物只写部署动作，不加入自动编队名单。纯治疗替换会失去遥原有攻击/支援效果；费用增加与提前部署重构体会改变后续到场时间。\n"
    "参考2026-11-20重新获取的一图流250条记录：Mon3tr符合配置；凛御银灰二、三技能均已专三，满足原S3专三要求。"
    "斩业星熊仍未持有，按作业已写要求可用单助战补齐其一技能、X模组配置；未降低原要求。\n"
    "已检查普通/突袭地块、原位、配置、容量、保留动作和静态链路；未连接游戏、未实战验证。"
)

roster_path = ROOT / "data/operators-2026-11-20.json"
box = {o["id"]: o for o in read(roster_path)}
own = box["char_4179_monstr"]
assert own["evolvePhase"] == 2 and own["level"] >= 60 and own["mainSkillLevel"] == 7
assert next(s for s in own["skills"] if s["id"] == "skchr_monstr_1")["level"] == 3
assert any(e["type"] == "X" and e["level"] == 3 for e in own["equips"])
assert skills["skchr_monstr_1"]["levels"][-1]["skillType"] == "AUTO"
assert "char_1044_hsgma2" not in box
assert box["char_1045_svash2"]["skills"][2]["level"] == 3
deploys = [a for a in job["actions"] if a["type"] == "Deploy" and a["name"] != "水汽汽水瓶"]
assert len(deploys) == len({tuple(a["location"]) for a in deploys}) == 7
for a in deploys:
    x, y = a["location"]
    for m in [mapdata, raid]:
        assert m["tiles"][y][x]["buildableType"] == (2 if a["name"] in ["Mon3tr", "圣聆初雪"] else 1)
    assert all(a["location"] != b["location"] for b in bottles)
assert job["groups"] == original["groups"]
assert [a for a in job["actions"] if a.get("name") == "水汽汽水瓶"] == bottles
assert [a for a in job["actions"] if a.get("name") not in ["Mon3tr", "重构体"]] == [
    a for a in original["actions"] if a.get("name") != "遥"]
assert all(o in job["opers"] for o in original["opers"] if o["name"] != "遥")
assert all(o["name"] not in ["遥", "重构体"] for o in job["opers"])
assert "skill_times" not in mon and mon["skill_usage"] == 0
assert not any(a["type"] in ["Skill", "SkillUsage"] and a.get("name") == "Mon3tr" for a in job["actions"])
assert len(deploys) + 1 <= stage["options"]["characterLimit"] == 8
assert job["difficulty"] == original["difficulty"] == 3
scenarios = []
for ratios in itertools.product([0.3, 0.6, 1.0], repeat=6):
    hp = dict(zip(local, ratios))
    for root in local:
        for enhanced in [False, True]:
            path = chain(root, ranks, hp, enhanced)
            scenarios.append({"root": root, "HP": ratios, "enhanced": enhanced,
                              "path": path, "ground_count": sum(g in path for g in ground)})
save("SL-EX-7-91823-Mon3tr-S1.json", job)
save("validation.json", {"stage": job["stage_name"], "difficulty": 3,
    "Mon3tr_original_position_and_direction": [2, 2, "Down"], "token": [1, 3, "Up"],
    "legal_free_token_tiles_with_original_bottle_reserved": legal_tokens,
    "game_auto_S1": True, "old_skill_times_removed": True,
    "original_other_actions_order_and_requirements_preserved": True,
    "original_robot_group_retained_undeployed": True, "early_token": True,
    "main_target_token_not_forced_by_S1": True, "direct_healing_area": sorted(area),
    "token_root_S1_equal_HP": chain("重构体", ranks),
    "token_root_normal_equal_HP": chain("重构体", ranks, enhanced=False),
    "per_chain_ground_coverage_guaranteed": False, "ulpianus_outside_chain": True,
    "roster_snapshot": roster_path.name,
    "roster_gaps": ["斩业星熊未持有"],
    "single_support_sufficient_for_snapshot": True, "scenario_count": len(scenarios),
    "HP_order": local, "scenarios": scenarios,
    "limits": "Fixed primary roots and HP ratios only; no HP updates, token decay, damage, healing amounts, cost timeline, or combat simulation.",
    "combat_verified": False})
save("placement-timing.json", {"fixed_Mon3tr": [2, 2, "Down"], "legal_tokens": legal_tokens,
    "timings": timings, "scoring": "token-root enhanced ground coverage, all-root equal-HP ground coverage, then earliest token"})
save("roster-reference.json", {"snapshot": roster_path.name, "refreshed_this_task": True,
    "snapshot_sha256": hashlib.sha256(roster_path.read_bytes()).hexdigest(), "Mon3tr": own,
    "SilverAsh": box["char_1045_svash2"], "Hoshiguma_owned": False})
print("Saved SL-EX-7-91823-Mon3tr-S1.json; original tile/actions preserved; 8748 fixed-root HP cases checked; combat not tested.")

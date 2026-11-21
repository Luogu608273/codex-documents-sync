"""Adapt SL-MO-1 with original-position S1 Mon3tr; no game execution."""
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
m = read(BASE / "map.json")
stage = read(BASE / "stage.raw.json")
characters = read(BASE / "character_table.json")
skills = read(BASE / "skill_table.json")
ranges = read(BASE / "range_table.json")
assert original["stage_name"] == m["stageId"] == "act27side_mo01"
levels = read(BASE / "levels.json")
assert any(s["stage_id"] == original["stage_name"] and s["cat_three"] == "SL-MO-1" for s in levels["data"])
positions = {a["name"]: tuple(a["location"]) for a in original["actions"] if a["type"] == "Deploy" and a["name"] != "遥"}
positions.update(Mon3tr=(4, 2))
original_names = ["凛御银灰", "圣聆初雪", "丰川祥子"]
ground = ["凛御银灰", "丰川祥子"]
area = {(4 + g["col"], 2 - g["row"]) for g in ranges["y-2"]["grids"]}
assert all(positions[n] in area for n in positions)
ranks = {"凛御银灰": 0, "Mon3tr": 1, "重构体": 2, "圣聆初雪": 3, "丰川祥子": 4}


def adjacent(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1])) <= 1


def chain(coords, root="重构体", hp=None, enhanced=False):
    """Fixed primary target/HP, 3 ordinary recipients (4 for S1), token +1."""
    hp = hp or {}
    path = [root]
    budget = (4 if enhanced else 3) + int(root == "重构体")
    while len(path) < budget:
        candidates = [n for n in coords if n not in path and adjacent(coords[path[-1]], coords[n])]
        if not candidates:
            break
        target = min(candidates, key=lambda n: (hp.get(n, 1.0), -ranks[n]))
        path.append(target)
        if target == "重构体":
            budget += 1
    return path


candidates = []
for x, y in sorted(area):
    if not (0 <= x < m["width"] and 0 <= y < m["height"]):
        continue
    if m["tiles"][y][x]["buildableType"] != 1 or (x, y) in positions.values():
        continue
    coords = dict(positions, 重构体=(x, y))
    full = chain(coords)
    injured = {g: chain(coords, hp={g: 0.3}) for g in ground}
    score = (sum(g in full for g in ground),
             sum(g in injured[g] for g in ground),
             sum(adjacent((x, y), positions[g]) for g in ground),
             sum(adjacent((x, y), positions[n]) for n in positions),
             sum(n in full for n in original_names), len(full))
    candidates.append({"token": [x, y], "score": score, "equal_HP": full, "single_injured_ground": injured})
candidates.sort(key=lambda v: v["score"], reverse=True)
assert candidates[0]["token"] == [4, 1]
positions["重构体"] = (4, 1)
full = chain(positions)
assert full == ["重构体", "丰川祥子", "Mon3tr", "凛御银灰"]
assert chain(positions, enhanced=True) == full
assert all(g in chain(positions, hp={g: 0.3}) for g in ground)
assert all(not adjacent(positions["圣聆初雪"], positions[n]) for n in positions if n != "圣聆初雪")
counterexample = chain(positions, hp={"Mon3tr": 0.3})
assert counterexample == ["重构体", "Mon3tr", "丰川祥子"]

mon = next(o for o in job["opers"] if o["name"] == "遥")
mon.clear()
mon.update(name="Mon3tr", role="medic", skill=1, skill_usage=0,
           requirements={"elite": 2, "level": 60, "skill_level": 10, "module": 1})
mon_index = next(i for i, a in enumerate(job["actions"]) if a.get("name") == "遥")
job["actions"][mon_index].update(name="Mon3tr", role="medic")
job["actions"].insert(mon_index + 1, {
    "type": "Deploy", "name": "重构体", "location": [4, 1], "direction": "Down",
    "doc": "Mon3tr之后立即部署；重构体持续失血，尽可能先治疗它，再串联祥子与银灰。",
})
job["minimum_required"] = "v6.18.0"
job["doc"]["title"] = "SL-MO-1 乡间路带我回家｜Mon3tr原位一技能与重构体（待实测）"
job["doc"]["details"] = original["doc"]["details"] + (
    "\n\n本地改写基于prts://96155，未修改线上作业。遥替换为医疗Mon3tr，保持原位(4,2)朝右。"
    "配置精二60、一技能专三、X模组三级；MAA模组类型1。一技能由游戏自动触发，skill_usage=0表示MAA无需点击，不禁止自动技能。\n"
    "Mon3tr落地后立即在(4,1)朝下部署重构体，随后继续原初雪、祥子动作。重构体仅写部署，不加入编队名单。"
    "其余三人技能、要求、坐标、方向、相对顺序均保留；凛御银灰三技能仍设好了就开。\n"
    "利用重构体持续失血尽可能先治疗重构体。一技能没有二技能强制优先治疗重构体的效果，其他单位血比更低时会先治疗其他单位。"
    "Mon3tr直接范围包含银灰(5,1)、祥子(3,1)、初雪(6,3)及重构体(4,1)。重构体周围八格同时覆盖银灰、祥子和Mon3tr。\n"
    "从重构体起链、后续候选同血比时：重构体→丰川祥子→Mon3tr→凛御银灰。祥子最后部署，故同血比优先于Mon3tr和银灰；"
    "祥子再经Mon3tr连接另一名地面干员银灰。该路线在普通治疗与一技能强化治疗下均有足够目标数，重构体为天赋额外跳跃目标。"
    "本布局优先两名地面，不把末端无法连接的初雪虚算进同一条链；初雪受伤时由Mon3tr直接治疗。\n"
    "每跳在周围八格按最低生命比例优先、同血比按后部署优先，单条链不重复治疗已经经过的目标。"
    "若Mon3tr自身血比最低，重构体可能先跳Mon3tr，再跳祥子后断链，遗漏银灰；不能保证每条链覆盖两名地面。"
    "不要额外部署其他单位或随意改顺序。\n"
    "关卡初始50费、自然每999秒才回1费，持续产费依赖凛御银灰三技能，不能停用。Mon3tr比遥更贵，并新增3费重构体，"
    "初雪与祥子的到场时间可能变化；原作业未部署汽水瓶，本版也不额外加瓶。替换还会失去遥的原攻击/支援效果。\n"
    "按精二基础费用、不计潜能减费，银灰13+Mon3tr18+重构体3后剩16费，不足初雪24费；原银灰13+遥13后剩24费。"
    "因此新版本可能在初雪尚待部署时触发银灰首次换费，初雪与祥子的换费参与情况会与原版不同，未模拟精确费用时轴。\n"
    "按2026-11-20一图流250条快照核对：Mon3tr符合配置；银灰S3专三高于原7级要求，初雪S2专三/Y模组三。"
    "丰川祥子未持有，需借原要求的二技能专三、Y模组版本；未擅自降低其要求。MAA只能检查模组类型，三级需手动核对。\n"
    "本关为SL-MO-1，原作业未设置difficulty字段，本版保持。已检查地图、技能类型、容量、原站位与静态治疗链，未实战验证。"
)

roster_path = ROOT / "data/operators-2026-11-20.json"
box = {o["id"]: o for o in read(roster_path)}
own = box["char_4179_monstr"]
assert own["evolvePhase"] == 2 and own["level"] >= 60 and own["mainSkillLevel"] == 7
assert next(s for s in own["skills"] if s["id"] == "skchr_monstr_1")["level"] == 3
assert any(e["type"] == "X" and e["level"] == 3 for e in own["equips"])
assert skills["skchr_monstr_1"]["levels"][-1]["skillType"] == "AUTO"
assert "char_4182_oblvns" not in box
assert box["char_1045_svash2"]["skills"][2]["level"] == 3
assert box["char_1046_sbell2"]["skills"][1]["level"] == 3
assert any(e["type"] == "Y" and e["level"] >= 1 for e in box["char_1046_sbell2"]["equips"])
deploys = [a for a in job["actions"] if a["type"] == "Deploy"]
assert len(deploys) == len({tuple(a["location"]) for a in deploys}) == 5
for a in deploys:
    x, y = a["location"]
    assert m["tiles"][y][x]["buildableType"] == (2 if a["name"] in ["Mon3tr", "圣聆初雪"] else 1)
assert len(deploys) <= stage["options"]["characterLimit"] == 9
assert stage["options"]["initialCost"] == 50 and stage["options"]["costIncreaseTime"] == 999
assert job.get("difficulty") == original.get("difficulty") is None
assert job["groups"] == original["groups"]
assert all(o in job["opers"] for o in original["opers"] if o["name"] != "遥")
assert [a for a in job["actions"] if a.get("name") not in ["Mon3tr", "重构体"]] == [a for a in original["actions"] if a.get("name") != "遥"]
old_deploy = next(a for a in original["actions"] if a.get("name") == "遥")
new_deploy = next(a for a in deploys if a["name"] == "Mon3tr")
assert old_deploy["location"] == new_deploy["location"] and old_deploy["direction"] == new_deploy["direction"]
assert all(o["name"] not in ["遥", "重构体"] for o in job["opers"])
assert not any(a["type"] in ["Skill", "SkillUsage"] and a.get("name") == "Mon3tr" for a in job["actions"])
local = list(positions)
scenarios = []
for ratios in itertools.product([0.3, 0.6, 1.0], repeat=5):
    hp = dict(zip(local, ratios))
    for root in local:
        for enhanced in [False, True]:
            path = chain(positions, root, hp, enhanced)
            scenarios.append({"root": root, "HP": ratios, "enhanced": enhanced,
                              "path": path, "ground_count": sum(g in path for g in ground)})
save("SL-MO-1-Mon3tr-S1.json", job)
save("placement-search.json", {"fixed_Mon3tr": [4, 2, "Right"], "candidates": candidates,
    "score_priority": ["ground_in_token_root_equal_HP", "single_injured_ground_reachable", "ground_in_token_aura", "allies_in_token_aura", "original_allies_in_chain", "chain_length"]})
save("validation.json", {"stage": job["stage_name"], "original_Mon3tr_tile_and_direction_preserved": True,
    "Mon3tr": [4, 2, "Right"], "token": [4, 1, "Down"], "game_auto_S1": True,
    "main_target_token_not_forced_by_S1": True, "direct_healing_area": sorted(area),
    "token_root_equal_HP": full, "Mon3tr_injured_counterexample": counterexample,
    "Pramanix_only_direct_healing": True, "ground_per_chain_guaranteed": False,
    "original_other_operators_actions_requirements_preserved": True, "legal_distinct_tiles": True,
    "deployment_count": 5, "deployment_limit": 9, "initial_DP": 50, "passive_DP_interval": 999,
    "base_cost_opening_review": {"remaining_after_original_SilverAsh_Haruka": 24,
        "remaining_after_new_SilverAsh_Mon3tr_token": 16, "Pramanix_base_cost": 24,
        "first_cost_swap_candidates_may_change": True, "potential_cost_reductions_not_modeled": True},
    "SilverAsh_S3_DP_generation_retained": True, "roster_snapshot": roster_path.name,
    "roster_gaps": ["丰川祥子未持有，需借S2专三/Y模组"], "single_support_sufficient_for_written_requirements": True,
    "HP_order": local, "scenario_count": len(scenarios), "scenarios": scenarios,
    "limits": "Fixed roots/HP only; no primary selection, HP updates, healing amounts, token survival, enemy combat or cost timeline simulation.",
    "combat_verified": False})
save("roster-reference.json", {"snapshot": roster_path.name, "refreshed_this_task": False,
    "snapshot_sha256": hashlib.sha256(roster_path.read_bytes()).hexdigest(), "Mon3tr": own,
    "SilverAsh": box["char_1045_svash2"], "Pramanix": box["char_1046_sbell2"], "Sakiko_owned": False})
print("Saved SL-MO-1-Mon3tr-S1.json; %d token candidates and %d HP/root cases checked; original positions retained; combat not tested." % (len(candidates), len(scenarios)))

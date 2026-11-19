"""Build the Mon3tr S2 job and compare static HP/order-dependent heal chains."""
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
mapdata = read(BASE / "map.json")
raidmap = read(BASE / "map-raid.json")
ranges = read(BASE / "range_table.json")
chars = read(BASE / "character_table.json")
skills = read(BASE / "skill_table.json")
equipment = read(BASE / "battle_equip_table.json")
stage = read(BASE / "stage.raw.json")
box = {o["id"]: o for o in read(ROOT / "data/operators-2026-11-19.json")}
assert original["stage_name"] == mapdata["stageId"] == "act39side_ex08"
assert mapdata["tiles"] == raidmap["tiles"]
jump_svg = (BASE / "jump-range.svg").read_text(encoding="utf-8")
assert 'viewbox="0 0 78 78"' in jump_svg.lower()
assert jump_svg.count('<use ') == 9 and jump_svg.count('xlink:href="#2"') == 8
fixed = {a["name"]: tuple(a["location"]) for a in original["actions"]
         if a["type"] == "Deploy" and a["name"] != "遥"}
right = ["歌蕾蒂娅", "圣聆初雪", "乌尔比安"]
ground = ["歌蕾蒂娅", "乌尔比安"]
order = {"斩业星熊": 0, "Mon3tr": 1, "歌蕾蒂娅": 2, "圣聆初雪": 3, "乌尔比安": 4, "重构体": 5}


def adjacent(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1])) <= 1


def heal_area(x, y, direction):
    result = set()
    for grid in ranges["y-2"]["grids"]:
        dx, dy = grid["col"], -grid["row"]
        if direction == "Left":
            dx, dy = -dx, -dy
        elif direction == "Up":
            dx, dy = dy, -dx
        elif direction == "Down":
            dx, dy = -dy, dx
        result.add((x + dx, y + dy))
    return result


def chain(positions, hp=None, ranks=None, budget=4):
    """S2 roots at the token; count token plus three other recipients.

    This is one chain, not an HP/healing/cooldown/combat simulation. Both the
    primary and the delayed S2 chain can re-evaluate priorities in actual play.
    """
    hp = hp or {}
    ranks = ranks or order
    path = ["重构体"]
    while len(path) < budget:
        options = [name for name in positions if name not in path and name != "斩业星熊"
                   and adjacent(positions[path[-1]], positions[name])]
        if not options:
            break
        path.append(min(options, key=lambda name: (hp.get(name, 1.0), -ranks[name])))
    return path


# Search only legal ordinary ground/high-ground tiles, preserving the other
# four operators' coordinates and relative deployment order.
candidates = []
for y, row in enumerate(mapdata["tiles"]):
    for x, tile in enumerate(row):
        if tile["buildableType"] != 2 or (x, y) in fixed.values():
            continue
        for direction in ["Up", "Down", "Left", "Right"]:
            area = heal_area(x, y, direction)
            for tx, ty in area:
                if not (0 <= tx < mapdata["width"] and 0 <= ty < mapdata["height"]):
                    continue
                if mapdata["tiles"][ty][tx]["buildableType"] != 1 or (tx, ty) in fixed.values():
                    continue
                positions = dict(fixed, Mon3tr=(x, y), 重构体=(tx, ty))
                full = chain(positions)
                injured = {g: chain(positions, {g: 0.3}) for g in ground}
                score = (
                    sum(g in injured[g] for g in ground),
                    sum(positions[g] in area for g in ground),
                    sum(g in full for g in ground),
                    sum(n in full for n in right),
                    sum(positions[n] in area for n in right),
                    sum(adjacent((tx, ty), positions[n]) for n in right),
                    int(adjacent((tx, ty), (x, y))),
                )
                candidates.append({"score": score, "Mon3tr": [x, y, direction],
                                   "token": [tx, ty], "full": full, "single_injured": injured})
candidates.sort(key=lambda value: value["score"], reverse=True)
winner = candidates[0]
assert winner["Mon3tr"] == [9, 5, "Down"] and winner["token"] == [9, 7]
assert len(candidates) == 251
positions = dict(fixed, Mon3tr=(9, 5), 重构体=(9, 7))
full = chain(positions)
assert full == ["重构体", "圣聆初雪", "Mon3tr", "乌尔比安"]
assert chain(positions, {"歌蕾蒂娅": 0.3}) == ["重构体", "歌蕾蒂娅"]
assert chain(positions, {"乌尔比安": 0.3}) == full
bad_order = dict(order, 歌蕾蒂娅=3, 圣聆初雪=2)
assert chain(positions, ranks=bad_order) == ["重构体", "歌蕾蒂娅"]
# The selected geometry gives the same examples even if "four jumps" is
# interpreted as four subsequent recipients after the token rather than four
# total recipients: no extra geometric link exists at the end of these paths.
assert chain(positions, budget=5) == full
assert chain(positions, {"歌蕾蒂娅": 0.3}, budget=5) == ["重构体", "歌蕾蒂娅"]

# In the preserved layout, Gladiia is a leaf reached only through the token.
# A no-repeat, token-rooted chain cannot include her and then continue to Ulpianus.
assert [n for n in positions if n != "歌蕾蒂娅" and adjacent(positions[n], positions["歌蕾蒂娅"])] == ["重构体"]
assert all(not adjacent(positions["斩业星熊"], positions[n]) for n in positions if n != "斩业星熊")

mon = next(o for o in job["opers"] if o["name"] == "遥")
mon.clear()
mon.update({"name": "Mon3tr", "role": "medic", "skill": 2, "skill_usage": 0,
            "requirements": {"elite": 2, "level": 60, "skill_level": 10, "module": 1}})
for action in job["actions"]:
    if action.get("name") == "遥":
        action.update(name="Mon3tr", role="medic", location=[9, 5], direction="Down")
speed_index = next(i for i, action in enumerate(job["actions"]) if action["type"] == "SpeedUp")
job["actions"][speed_index:speed_index] = [
    {"type": "Deploy", "name": "重构体", "location": [9, 7], "direction": "Up",
     "doc": "满血路径：重构体→初雪→Mon3tr→乌尔比安；歌蕾蒂娅掉血时优先跳向她。"},
    {"type": "SkillUsage", "name": "Mon3tr", "role": "medic", "skill_usage": 1,
     "doc": "重构体就位后，Mon3tr二技能好了就开。"},
]
job["minimum_required"] = "v6.18.0"
job["doc"]["title"] = "EP-EX-8 盐海尽头｜Mon3tr二技能链愈适配（待实测）"
job["doc"]["details"] = (
    original["doc"]["details"]
    + "\n\n本地修改版，基于prts://77980，未覆盖线上原作业。\n"
    "遥替换为Mon3tr：精二60、二技能专三、X模组三级，MAA坐标(9,5)朝下。"
    "重构体放(9,7)朝上，在原五名干员部署完成后追加。随后启用Mon3tr二技能好了就用，再二倍速挂机。"
    "初始skill_usage=0是为了等重构体就位，后续SkillUsage动作改为1，不限制开技次数。\n"
    "不要额外部署其他单位或随意改变部署顺序，否则同血比选择和治疗链会改变。\n"
    "其他四人坐标与相对顺序不变；用户指定斩业星熊不纳入治疗覆盖目标，仍保留其原阵容与部署。"
    "本次只替换遥并新增重构体，不增加其他治疗跳板。\n"
    "Mon3tr直接治疗范围包含右侧歌蕾蒂娅(10,7)、初雪(8,6)、乌尔比安(9,4)和重构体(9,7)。"
    "二技能优先以重构体起链，每跳按低血量比例优先、同血量比例后部署优先，不重复跳已治疗目标。\n"
    "保持歌蕾蒂娅先于初雪部署；全员满血/同血比时，重构体先选后部署的初雪，"
    "再经Mon3tr本人中转抵达乌尔比安：重构体→初雪→Mon3tr→乌尔比安。"
    "若把歌蕾蒂娅移到初雪之后部署，满血时会先跳歌蕾蒂娅并断在右下角。\n"
    "歌蕾蒂娅血比更低时会优先走重构体→歌蕾蒂娅，保障掉血地面单位。"
    "她仅与重构体相邻，单条链不能从她继续跳到乌尔比安；不能保证每条链同时覆盖两名地面干员。"
    "若歌蕾蒂娅轻伤而乌尔比安重伤，重构体仍只能比较其相邻候选，可能先跳歌蕾蒂娅。"
    "实际治疗后血量变化、二技能延迟追加链、技能空档和敌方攻击都会改变后续链路。\n"
    "重构体邻接初雪和歌蕾蒂娅，提供攻击力增益；Mon3tr与乌尔比安不在其周围八格。"
    "重构体是召唤物，仅写部署动作，不加入自动编队名单。\n"
    "2026-11-19一图流确认Mon3tr为精二60、S2专三、X模组三级；模组等级需手动核对。"
    "当前快照未持有斩业星熊，仍需按原作业准备/借用二技能斩业星熊。"
    "歌蕾蒂娅自有一技能7级，原作业未写专精门槛，不能据此确认7级一定可通关。\n"
    "比较了251个合法位置/朝向/召唤物组合，并做血比与部署顺序的静态检查；未连接游戏，未实战验证。"
)

own = box["char_4179_monstr"]
assert own["evolvePhase"] == 2 and own["level"] >= 60
assert own["mainSkillLevel"] == 7 and own["skills"][1]["level"] == 3
assert any(e["type"] == "X" and e["level"] == 3 for e in own["equips"])
assert skills["skchr_monstr_2"]["levels"][-1]["skillType"] == "MANUAL"
trait = equipment["uniequip_002_monstr"]["phases"][2]["parts"][0]
assert trait["overrideTraitDataBundle"]["candidates"][0]["blackboard"][0]["value"] == 3
assert "char_1044_hsgma2" not in box
deploys = [a for a in job["actions"] if a["type"] == "Deploy"]
assert [a["name"] for a in deploys] == ["斩业星熊", "Mon3tr", "歌蕾蒂娅", "圣聆初雪", "乌尔比安", "重构体"]
assert len({tuple(a["location"]) for a in deploys}) == len(deploys) == 6
for action in deploys:
    x, y = action["location"]
    expected = 2 if action["name"] in ["Mon3tr", "圣聆初雪"] else 1
    assert mapdata["tiles"][y][x]["buildableType"] == expected
    assert raidmap["tiles"][y][x]["buildableType"] == expected
    assert mapdata["tiles"][y][x]["tileKey"] not in ["tile_sandrope", "tile_sandrope_2", "tile_quicksand"]
assert positions["重构体"] in heal_area(9, 5, "Down")
assert all(positions[n] in heal_area(9, 5, "Down") for n in right)
assert all(o["name"] not in ["遥", "重构体"] for o in job["opers"])
for old in original["opers"]:
    if old["name"] != "遥":
        assert old in job["opers"]
for old in original["actions"]:
    if old.get("name") in fixed:
        assert old in job["actions"]
assert job["difficulty"] == original["difficulty"] == 3
assert len(deploys) <= stage["options"]["characterLimit"] == 8

scenarios = []
for ratios in itertools.product([0.3, 0.6, 1.0], repeat=4):
    hp = dict(zip(right + ["Mon3tr"], ratios))
    path = chain(positions, hp)
    scenarios.append({"hp_ratios": hp, "path": path, "ground_recipients": [g for g in ground if g in path]})
save("EP-EX-8-Mon3tr-S2.json", job)
save("placement-search.json", {"candidate_count": len(candidates), "top": candidates[:24],
    "fixed_coordinates": fixed, "deployment_order": order,
    "score_priority": ["injured_ground_reachable", "ground_in_direct_range", "ground_in_full_HP_chain",
                       "original_allies_in_full_HP_chain", "allies_in_direct_range", "token_aura_targets", "caster_in_token_aura"]})
save("validation.json", {"stage": job["stage_name"], "difficulty": job["difficulty"],
    "legal_distinct_deployment_tiles": True, "other_four_positions_preserved": True,
    "Mon3tr": [9, 5, "Down"], "reconstruction": [9, 7, "Up"], "skill_usage_after_token": 1,
    "direct_healing_range": sorted(heal_area(9, 5, "Down")), "all_three_right_allies_in_direct_range": True,
    "jump_neighborhood": "3x3; PRTS SVG verified separately", "target_budget_including_token": 4,
    "full_HP_chain": full, "gladiia_lower_HP_chain": chain(positions, {"歌蕾蒂娅": 0.3}),
    "bad_equal_HP_order_chain": chain(positions, ranks=bad_order),
    "scenarios": scenarios, "joint_ground_coverage_per_chain_guaranteed": False,
    "hoshiguma_excluded_from_healing_objective": True, "hoshiguma_still_in_roster": True,
    "support_needed": "斩业星熊", "Mon3tr_owned_requirements_met": True,
    "combat_verified": False, "core_loaded": False,
    "limits": "Static recipient selection only. Does not model healing amounts, target selection while S2 is inactive, animation, delayed echo HP updates, enemy damage, or summon survival."})
raw = ROOT / "data/operators-2026-11-19.raw.json"
save("roster-reference.json", {"snapshot": "operators-2026-11-19.json", "count": len(box),
    "raw_sha256": hashlib.sha256(raw.read_bytes()).hexdigest(), "Mon3tr": own,
    "source": "https://backend.yituliu.cn/open-api/operator/info", "game_sync_time": "not provided"})
print("Saved EP-EX-8-Mon3tr-S2.json; 251 placements compared, 81 HP scenarios checked; original allies preserved; combat not tested.")

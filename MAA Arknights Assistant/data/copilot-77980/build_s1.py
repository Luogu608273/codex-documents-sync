"""Create the requested S1 variant without changing deployment positions/order."""
import copy
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def save(name, value):
    (BASE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


previous = read(BASE / "EP-EX-8-Mon3tr-S2.json")
original = read(BASE / "original.json")
job = copy.deepcopy(previous)
mon = next(o for o in job["opers"] if o["name"] == "Mon3tr")
mon.update(skill=1, skill_usage=0)
job["actions"] = [a for a in job["actions"]
                  if not (a.get("name") == "Mon3tr" and a["type"] == "SkillUsage")]
token = next(a for a in job["actions"] if a.get("name") == "重构体")
token["doc"] = "重构体最后部署于(9,7)，邻接歌蕾蒂娅和圣聆初雪，可参与治疗链与提供增益。"
job["doc"]["title"] = "EP-EX-8 盐海尽头｜Mon3tr一技能适配（待实测）"
job["doc"]["details"] = original["doc"]["details"] + (
    "\n\n本地修改版，基于prts://77980，按用户要求将Mon3tr改为一技能。"
    "遥替换为医疗Mon3tr：精二60、一技能专三、X模组三级，MAA坐标(9,5)朝下。"
    "重构体仍放(9,7)朝上，最后部署；其余四名干员的配置、坐标、朝向及相对顺序保持。\n"
    "一技能为攻击回复、自动触发，无需MAA手动点击，skill_usage=0不阻止游戏自动触发。"
    "移除原二技能的SkillUsage动作，不再等待重构体落地才开技。\n"
    "Mon3tr直接治疗范围仍包含歌蕾蒂娅(10,7)、圣聆初雪(8,6)、乌尔比安(9,4)和重构体(9,7)。"
    "一技能没有二技能优先治疗重构体与延迟追加治疗链的效果；原二技能以重构体固定起链的说明不适用。"
    "实际链路受受伤目标、各次治疗后的血量比例与部署顺序影响，不能保证每次同时覆盖两名地面干员。"
    "不要额外部署单位或随意改变部署顺序。\n"
    "斩业星熊保留原位，按用户要求不纳入治疗覆盖目标。"
    "重构体邻接歌蕾蒂娅和圣聆初雪，不邻接Mon3tr及乌尔比安；召唤物只写部署动作，不加入编队名单。\n"
    "2026-11-19一图流快照确认Mon3tr精二60、一技能专三、X模组三级；MAA模组类型设为1。"
    "快照未持有斩业星熊，仍需按原作业准备/借用其二技能。"
    "歌蕾蒂娅自有一技能7级，原作业未写专精门槛，不能据此确认可通关。\n"
    "已检查技能自动触发类型、干员配置、原部署顺序及普通/突袭地块合法性，未实战验证。"
)

skill = read(BASE / "skill_table.json")["skchr_monstr_1"]["levels"][-1]
assert skill["skillType"] == "AUTO" and skill["rangeId"] == "y-2"
roster = read(BASE.parents[1] / "data/operators-2026-11-19.json")
own = next(o for o in roster if o["id"] == "char_4179_monstr")
assert own["evolvePhase"] == 2 and own["level"] >= 60
assert own["mainSkillLevel"] == 7
assert next(s for s in own["skills"] if s["id"] == "skchr_monstr_1")["level"] == 3
assert any(e["type"] == "X" and e["level"] == 3 for e in own["equips"])
deploys = [a for a in job["actions"] if a["type"] == "Deploy"]
assert [(a["name"], a["location"], a["direction"]) for a in deploys] == [
    (a["name"], a["location"], a["direction"]) for a in previous["actions"] if a["type"] == "Deploy"]
assert len(deploys) == len({tuple(a["location"]) for a in deploys}) == 6
for mapname in ["map.json", "map-raid.json"]:
    tiles = read(BASE / mapname)["tiles"]
    for a in deploys:
        x, y = a["location"]
        assert tiles[y][x]["buildableType"] == (2 if a["name"] in ["Mon3tr", "圣聆初雪"] else 1)
assert len(deploys) <= read(BASE / "stage.raw.json")["options"]["characterLimit"]
assert job["difficulty"] == original["difficulty"] == 3
assert all(o in job["opers"] for o in original["opers"] if o["name"] != "遥")
assert all(o["name"] not in ["遥", "重构体"] for o in job["opers"])
assert not any(a["type"] in ["Skill", "SkillUsage"] and a.get("name") == "Mon3tr" for a in job["actions"])
save("EP-EX-8-Mon3tr-S1.json", job)
save("validation-S1.json", {
    "job": "EP-EX-8-Mon3tr-S1.json", "skill": 1, "skill_type": skill["skillType"],
    "automatic_in_game": True, "manual_skill_actions": 0, "owned_requirements_met": True,
    "deployments_unchanged_from_S2": True, "legal_normal_and_raid_tiles": True,
    "distinct_deployments": len(deploys), "hoshiguma_excluded_from_healing_objective": True,
    "s2_token_priority_and_delayed_chain_not_applicable": True,
    "combat_verified": False,
})
print("Saved EP-EX-8-Mon3tr-S1.json; S1 AUTO verified; six deployments preserved; combat not tested.")

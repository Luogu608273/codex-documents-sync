#!/usr/bin/env python3
"""Read public PRTS Plus jobs; resolve display codes before querying. No execution."""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

BASE = "https://prts.maa.plus"


def get_json(path, params=None):
    url = BASE + path
    if params:
        url += "?" + urlencode(params)
    request = Request(url, headers={"Accept": "application/json",
                                    "User-Agent": "ArknightsHomeworkSkill/1.0"})
    with urlopen(request, timeout=25) as response:
        body = json.load(response)
    if not isinstance(body, dict) or body.get("status_code") != 200:
        raise ValueError(f"API failed: {path}: {body.get('message') if isinstance(body, dict) else 'invalid response'}")
    if body.get("data") is None:
        raise ValueError(f"Missing data: {path}")
    return body["data"]


def base_stage(stage_id):
    return stage_id.removesuffix("#f#").replace("bossrush_tm", "bossrush_")


def resolve_stage(levels, stage=None, stage_id=None, category=None):
    if not isinstance(levels, list):
        raise ValueError("Level API did not return an array")
    matches = []
    for level in levels:
        if not isinstance(level, dict):
            raise ValueError("Invalid level record")
        if stage_id:
            matched = level.get("stage_id") == stage_id
        else:
            matched = str(level.get("cat_three", "")).upper() == stage.upper()
        if matched and (not category or category in str(level.get("cat_two", ""))):
            matches.append(level)
    if not matches:
        raise ValueError("No exact stage found. Verify code/category/ID; do not invent an ID.")
    bases = {base_stage(level["stage_id"]) for level in matches}
    if len(bases) != 1:
        choices = [{key: level.get(key) for key in ("stage_id", "cat_two", "cat_three", "name")}
                   for level in matches]
        raise ValueError("Ambiguous stage; use --category or --stage-id: "
                         + json.dumps(choices, ensure_ascii=False))
    return stage_id or next(iter(bases)), matches


def search_jobs(stage_id, pages=1, limit=50, document=None):
    jobs, invalid, seen = [], [], set()
    total, has_next, fetched_pages = 0, False, 0
    for page in range(1, pages + 1):
        params = {"levelKeyword": stage_id, "page": page, "limit": limit,
                  "orderBy": "hot", "desc": "true"}
        if document:
            params["document"] = document
        data = get_json("/copilot/query", params)
        if (not isinstance(data, dict) or not isinstance(data.get("data"), list)
                or not isinstance(data.get("has_next"), bool)
                or not isinstance(data.get("total"), int)
                or data.get("page") != page):
            raise ValueError("Unexpected pagination schema or page number")
        total, has_next, fetched_pages = data["total"], data["has_next"], page
        if has_next and not data["data"]:
            raise ValueError("Empty page claims more pages; stop and review API behavior")
        for job in data["data"]:
            if not isinstance(job, dict) or not isinstance(job.get("id"), int):
                raise ValueError("Invalid job record")
            if job["id"] in seen:
                continue
            seen.add(job["id"])
            if job.get("type") != "PRTS":
                invalid.append({"id": job["id"], "reason": "not a PRTS JSON job"})
                continue
            try:
                content = json.loads(job["content"])
            except (KeyError, TypeError, json.JSONDecodeError) as exc:
                invalid.append({"id": job["id"], "reason": str(exc)})
                continue
            if not isinstance(content, dict) or not isinstance(content.get("stage_name"), str):
                invalid.append({"id": job["id"], "reason": "missing stage_name"})
                continue
            if base_stage(content["stage_name"]) != base_stage(stage_id):
                raise ValueError(f"Unexpected stage in job {job['id']}: "
                                 f"{content['stage_name']!r}; requested {stage_id!r}. "
                                 "Stop; do not treat these results as a match.")
            jobs.append({**job, "content": content,
                         "url": f"https://prts.plus/?op={job['id']}"})
        if not has_next:
            break
    return {"stage_id": stage_id, "server_total": total, "fetched_pages": fetched_pages,
            "has_next": has_next, "truncated": has_next, "unique_fetched": len(seen),
            "job_count": len(jobs), "invalid_or_other_type": invalid, "jobs": jobs,
            "difficulty_review_required": True,
            "note": "关卡匹配仅核对内部 ID 的关卡族；普通/困难及 difficulty 字段仍须逐条复核。未执行干员匹配或作业。",
            "fetched_at_utc": datetime.now(timezone.utc).isoformat()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--stage", help="显示关卡编号，例如 1-7")
    group.add_argument("--stage-id", help="已核实的内部关卡 ID")
    parser.add_argument("--category", help="活动/章节名称子串，用于消除编号歧义")
    parser.add_argument("--document", help="额外的标题/说明关键词")
    parser.add_argument("--pages", type=int, default=1)
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--output", type=Path, help="保存结果；拒绝覆盖已有文件")
    args = parser.parse_args()
    if not 1 <= args.limit <= 50 or not 1 <= args.pages <= 20:
        parser.error("limit 必须为 1～50，pages 必须为 1～20")
    if args.output and args.output.exists():
        parser.error("输出文件已存在，请另选文件名")
    levels = get_json("/arknights/level")
    stage_id, levels = resolve_stage(levels, args.stage, args.stage_id, args.category)
    result = search_jobs(stage_id, args.pages, args.limit, args.document)
    result["levels"] = levels
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("x", encoding="utf-8") as output:
            output.write(text + "\n")
        print(json.dumps({"saved": str(args.output.resolve()), "stage_id": stage_id,
                          "jobs": result["job_count"], "server_total": result["server_total"],
                          "truncated": result["truncated"]}, ensure_ascii=False))
    else:
        print(text)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"查询失败：{error}", file=sys.stderr)
        sys.exit(1)

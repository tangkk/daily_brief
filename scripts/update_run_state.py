#!/usr/bin/env python3
import argparse
import json
import pathlib
from datetime import datetime
from zoneinfo import ZoneInfo

MILESTONES = [
    "started",
    "research_complete",
    "written_staged",
    "spoken_committed",
    "podcast_verified",
    "written_published",
    "published_verified",
]

TIMESTAMP_KEYS = {
    "research_complete": "research_completed_at",
    "written_staged": "written_staged_at",
    "spoken_committed": "spoken_committed_at",
    "podcast_verified": "podcast_verified_at",
    "written_published": "written_published_at",
    "published_verified": "published_verified_at",
}


def reached(current: str, target: str) -> bool:
    return MILESTONES.index(current) >= MILESTONES.index(target)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--date", required=True)
    p.add_argument("--status", required=True, choices=MILESTONES)
    p.add_argument("--root", default=".")
    args = p.parse_args()

    path = pathlib.Path(args.root) / "ops" / "daily-brief-runs" / f"{args.date}.json"
    data = {}
    if path.exists():
        data = json.loads(path.read_text(encoding="utf-8"))

    now = datetime.now(ZoneInfo("Asia/Shanghai")).replace(microsecond=0).isoformat()
    previous = data.get("status", "started")
    if previous not in MILESTONES:
        previous = "started"

    # Never regress a durable checkpoint.
    status = args.status if MILESTONES.index(args.status) >= MILESTONES.index(previous) else previous

    data["date"] = args.date
    data.setdefault("run_type", "daily_brief")
    data["status"] = status
    data.setdefault("started_at", now)

    state = data.setdefault("artifact_state", {})
    state["written_draft"] = reached(status, "written_staged")
    state["spoken_canonical"] = reached(status, "spoken_committed")
    state["podcast_verified"] = reached(status, "podcast_verified")
    state["written_published"] = reached(status, "written_published")
    state["published_verified"] = reached(status, "published_verified")

    key = TIMESTAMP_KEYS.get(args.status)
    if key:
        data.setdefault(key, now)
    data["updated_at"] = now

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

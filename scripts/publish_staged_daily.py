#!/usr/bin/env python3
import argparse
import json
import pathlib
import re
import shutil
import sys
import xml.etree.ElementTree as ET

ITUNES = "http://www.itunes.com/dtds/podcast-1.0.dtd"


def find_episode(feed_path: pathlib.Path, date: str):
    tree = ET.parse(feed_path)
    channel = tree.getroot().find("channel")
    if channel is None:
        raise RuntimeError("RSS channel missing")
    pattern = re.compile(rf"^ep\d+-daily-{re.escape(date)}$")
    items = [i for i in channel.findall("item") if pattern.match(i.findtext("guid") or "")]
    if len(items) != 1:
        raise RuntimeError(f"expected exactly one Podcast item for {date}, got {len(items)}")
    item = items[0]
    enclosure = item.find("enclosure")
    if enclosure is None:
        raise RuntimeError("RSS enclosure missing")
    url = enclosure.attrib.get("url", "").strip()
    length = enclosure.attrib.get("length", "").strip()
    duration = item.findtext(f"{{{ITUNES}}}duration", default="").strip()
    if not url or not length.isdigit() or int(length) <= 0 or not duration:
        raise RuntimeError("RSS item has incomplete final audio metadata")
    title = (item.findtext("title") or "").strip()
    return url, int(length), duration, title


def validate_daily_file(path: pathlib.Path):
    text = path.read_text(encoding="utf-8")
    if not re.search(r"(?m)^layout:\s*daily_brief\s*$", text):
        raise RuntimeError(f"not a Daily Brief file: {path}")
    return text


def sync_title(path: pathlib.Path, title: str):
    """Give the written post the same title as its podcast episode."""
    if "｜" not in title or title.startswith("龙虾日报"):
        return
    text = path.read_text(encoding="utf-8")
    line = "title: " + json.dumps(title, ensure_ascii=False)
    new, n = re.subn(r"(?m)^title:.*$", lambda _: line, text, count=1)
    if n == 0:
        new = re.sub(r"(?m)^layout:\s*daily_brief\s*$", lambda m: m.group(0) + "\n" + line, text, count=1)
    if new != text:
        path.write_text(new, encoding="utf-8")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--date", required=True)
    p.add_argument("--feed", required=True)
    p.add_argument("--root", default=".")
    p.add_argument("--check-only", action="store_true")
    args = p.parse_args()

    root = pathlib.Path(args.root)
    feed = pathlib.Path(args.feed)
    url, length, duration, title = find_episode(feed, args.date)

    if args.check_only:
        print(json.dumps({"url": url, "length": length, "duration": duration}, ensure_ascii=False))
        return 0

    draft = root / "_drafts" / f"{args.date}-daily-brief.md"
    post = root / "_posts" / f"{args.date}-daily-brief.md"

    if draft.exists():
        validate_daily_file(draft)
        post.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(draft), str(post))
    elif post.exists():
        validate_daily_file(post)
    else:
        raise RuntimeError(f"written draft/post missing for {args.date}")
    sync_title(post, title)

    audio_path = root / "_data" / "audio.json"
    audio = json.loads(audio_path.read_text(encoding="utf-8"))
    audio[args.date] = url
    audio_path.write_text(
        json.dumps(audio, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    print(json.dumps({"url": url, "length": length, "duration": duration}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(2)

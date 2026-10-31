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



def validate_editorial_structure(path: pathlib.Path, date: str, root: pathlib.Path, podcast_title: str):
    """Fail closed before publishing a structurally inconsistent dated edition."""
    import datetime
    text = validate_daily_file(path)
    if datetime.date.fromisoformat(date).weekday() != 6:
        section = re.search(r"(?ms)^## Top Headlines[ \t]*\n(.*?)(?=^## |\Z)", text)
        if section is None:
            raise RuntimeError("Top Headlines section missing")
        numbers = [int(x) for x in re.findall(r"(?m)^### (\d+)\. ", section.group(1))]
        if len(numbers) < 6 or numbers != list(range(1, len(numbers) + 1)):
            raise RuntimeError(f"Top Headlines must have six or more consecutive headings from 1; got {numbers}")
    # Require the weekday number or Sunday weekly number, without judging editorial relevance.
    sunday = datetime.date.fromisoformat(date).weekday() == 6
    number_heading = "本周数字" if sunday else "Number of the Day / 今日数字"
    number_section = re.search(r"(?ms)^## " + re.escape(number_heading) + r"[ \t]*\n(.*?)(?=^## |\Z)", text)
    if number_section is None or not re.search(r"\*\*[^*]+\*\*", number_section.group(1)):
        raise RuntimeError(f"{number_heading} missing or has no highlighted figure")
    stress_path = root / "handoffs" / f"{date}-stress.json"
    if stress_path.exists():
        reading = json.loads(stress_path.read_text(encoding="utf-8"))
        value = reading.get("index")
        if not isinstance(value, (int, float)):
            raise RuntimeError("Stress index reading is invalid")
        market = re.search(r"(?ms)^## Markets Dashboard\s*\n(.*?)(?=^## |\Z)", text)
        if market is None or not re.search(r"龙虾压力指数[^\n]*" + re.escape(f"{value:.1f}"), market.group(1)):
            raise RuntimeError("Markets Dashboard stress reading disagrees with dated stress handoff")
        if podcast_title and f"压力指数 {int(value + 0.5)}" not in podcast_title:
            raise RuntimeError("Podcast title pressure-index suffix disagrees with stress handoff")
    headline_match = re.search(r'(?m)^headline:\s*"([^"]*)"\s*$', text)
    handoff_path = root / "handoffs" / f"{date}-title.txt"
    if handoff_path.exists():
        handoff = handoff_path.read_text(encoding="utf-8").strip()
        if headline_match and headline_match.group(1) != handoff:
            raise RuntimeError("Written headline and handoff title differ")
        if podcast_title and handoff not in podcast_title:
            raise RuntimeError("Podcast RSS title does not contain canonical handoff headline")


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

    draft = root / "_drafts" / f"{args.date}-daily-brief.md"
    post = root / "_posts" / f"{args.date}-daily-brief.md"
    target = draft if draft.exists() else post
    if target.exists():
        validate_editorial_structure(target, args.date, root, title)

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
, text)
    handoff_path = root / "handoffs" / f"{date}-title.txt"
    if handoff_path.exists():
        handoff = handoff_path.read_text(encoding="utf-8").strip()
        if headline_match and headline_match.group(1) != handoff:
            raise RuntimeError("Written headline and handoff title differ")
        if podcast_title and handoff not in podcast_title:
            raise RuntimeError("Podcast RSS title does not contain canonical handoff headline")


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

    draft = root / "_drafts" / f"{args.date}-daily-brief.md"
    post = root / "_posts" / f"{args.date}-daily-brief.md"
    target = draft if draft.exists() else post
    if target.exists():
        validate_editorial_structure(target, args.date, root, title)

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

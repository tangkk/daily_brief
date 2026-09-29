#!/usr/bin/env python3
import argparse
import json
import pathlib
import re
import sys
import xml.etree.ElementTree as ET

ITUNES = "http://www.itunes.com/dtds/podcast-1.0.dtd"


def podcast_item(feed_path: pathlib.Path, date: str):
    if not feed_path.exists():
        return None, "feed_missing"
    try:
        tree = ET.parse(feed_path)
    except Exception as exc:
        return None, f"feed_invalid:{exc}"
    channel = tree.getroot().find("channel")
    if channel is None:
        return None, "channel_missing"
    pat = re.compile(rf"^ep\d+-daily-{re.escape(date)}$")
    items = [i for i in channel.findall("item") if pat.match(i.findtext("guid") or "")]
    if len(items) == 0:
        return None, "podcast_item_missing"
    if len(items) != 1:
        return None, f"podcast_item_count:{len(items)}"
    item = items[0]
    enclosure = item.find("enclosure")
    if enclosure is None:
        return None, "enclosure_missing"
    url = enclosure.attrib.get("url", "").strip()
    length = enclosure.attrib.get("length", "").strip()
    duration = item.findtext(f"{{{ITUNES}}}duration", default="").strip()
    if not url or not length.isdigit() or int(length) <= 0 or not duration:
        return None, "podcast_metadata_incomplete"
    return {
        "guid": item.findtext("guid"),
        "url": url,
        "length": int(length),
        "duration": duration,
    }, None


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--date", required=True)
    p.add_argument("--feed", required=True)
    p.add_argument("--root", default=".")
    p.add_argument("--live-html", default=None,
                   help="Optional saved HTML fixture for public-page verification; never fetches the network.")
    args = p.parse_args()

    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", args.date):
        raise SystemExit("bad date")

    root = pathlib.Path(args.root)
    feed = pathlib.Path(args.feed)
    draft = root / "_drafts" / f"{args.date}-daily-brief.md"
    post = root / "_posts" / f"{args.date}-daily-brief.md"
    audio_path = root / "_data" / "audio.json"

    item, podcast_error = podcast_item(feed, args.date)
    podcast_verified = item is not None

    audio = {}
    if audio_path.exists():
        try:
            audio = json.loads(audio_path.read_text(encoding="utf-8"))
        except Exception:
            audio = {}
    mapped = audio.get(args.date)
    mapping_match = bool(item and mapped == item["url"])

    live_verified = None
    if args.live_html is not None:
        html_path = pathlib.Path(args.live_html)
        html = html_path.read_text(encoding="utf-8") if html_path.exists() else ""
        live_verified = bool(
            item
            and f"<h1>{args.date}</h1>" in html
            and item["url"] in html
        )

    if podcast_verified and post.exists() and mapping_match and (live_verified is not False):
        final_state = "published_verified" if live_verified is True else "written_published"
    elif podcast_verified and post.exists():
        final_state = "written_published"
    elif podcast_verified:
        final_state = "podcast_verified"
    elif draft.exists():
        final_state = "written_staged"
    else:
        final_state = "started"

    result = {
        "date": args.date,
        "final_state": final_state,
        "written_draft": draft.exists(),
        "written_post": post.exists(),
        "podcast_verified": podcast_verified,
        "podcast_error": podcast_error,
        "guid": item["guid"] if item else None,
        "enclosure_url": item["url"] if item else None,
        "audio_mapping": mapped,
        "audio_mapping_match": mapping_match,
        "live_verified": live_verified,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))

    # This checker reports state; inconsistent public state is a validation failure.
    if post.exists() and podcast_verified and not mapping_match:
        return 3
    if live_verified is False:
        return 4
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

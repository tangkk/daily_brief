# -*- coding: utf-8 -*-
import argparse
import html
import json
import re
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

import imageio_ffmpeg

from tts_normalize import normalize_for_tts
from xfyun_tts import DEFAULT_URL, DEFAULT_VOICE, run_once


MAX_CHARS = 1800


def strip_front_matter(text: str) -> str:
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            return parts[2].lstrip()
    return text


def markdown_to_spoken_text(markdown: str) -> str:
    """Strip Markdown/rendering syntax, then apply deterministic TTS normalization."""
    text = strip_front_matter(markdown)
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"https?://\S+", "", text)
    text = re.sub(r"^#{1,6}\s*", "", text, flags=re.M)
    text = re.sub(r"^>\s?", "", text, flags=re.M)
    text = re.sub(r"^[-*+]\s+", "", text, flags=re.M)
    text = re.sub(r"^\s*\d+\.\s+", "", text, flags=re.M)
    text = text.replace("**", "").replace("__", "").replace("`", "")
    text = html.unescape(text)

    paragraphs = []
    for p in re.split(r"\n\s*\n", text):
        p = re.sub(r"\s+", " ", p).strip()
        if p:
            paragraphs.append(p)
    return normalize_for_tts("\n\n".join(paragraphs))


def split_long_piece(piece: str, limit: int):
    if len(piece) <= limit:
        return [piece]
    out = []
    rest = piece.strip()
    while len(rest) > limit:
        cut = -1
        for punct in "。！？；，,.!?;：:":
            pos = rest.rfind(punct, 0, limit + 1)
            cut = max(cut, pos)
        if cut < int(limit * 0.55):
            cut = limit
        else:
            cut += 1
        out.append(rest[:cut].strip())
        rest = rest[cut:].strip()
    if rest:
        out.append(rest)
    return out


def split_text(text: str, limit: int = MAX_CHARS):
    units = []
    for paragraph in text.split("\n\n"):
        paragraph = paragraph.strip()
        if not paragraph:
            continue
        sentences = [s.strip() for s in re.split(r"(?<=[。！？!?])\s*", paragraph) if s.strip()]
        if not sentences:
            sentences = [paragraph]
        for sentence in sentences:
            units.extend(split_long_piece(sentence, limit))

    chunks = []
    current = ""
    for unit in units:
        candidate = unit if not current else current + "\n" + unit
        if len(candidate) <= limit:
            current = candidate
        else:
            if current:
                chunks.append(current)
            current = unit
    if current:
        chunks.append(current)
    return chunks


def synthesize_chunk(text, out_path, voice, speed, volume, pitch, requrl, retries=3):
    last_error = None
    for attempt in range(1, retries + 1):
        try:
            return run_once(
                str(out_path), text, voice=voice, speed=speed, volume=volume,
                pitch=pitch, requrl=requrl,
            )
        except Exception as exc:
            last_error = exc
            if attempt < retries:
                time.sleep(2 * attempt)
    raise RuntimeError(f"TTS failed after {retries} attempts: {last_error}")


def concat_mp3(parts, out_path):
    if not parts:
        raise RuntimeError("No audio chunks to concatenate")
    if len(parts) == 1:
        shutil.copyfile(parts[0], out_path)
        return

    list_file = out_path.parent / "concat.txt"
    with list_file.open("w", encoding="utf-8") as f:
        for part in parts:
            safe = str(part.resolve()).replace("'", "'\\''")
            f.write(f"file '{safe}'\n")

    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    print(f"Using ffmpeg: {ffmpeg_exe}")
    subprocess.run(
        [ffmpeg_exe, "-hide_banner", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0",
         "-i", str(list_file), "-c", "copy", str(out_path)],
        check=True,
    )


def post_date(post_path: Path) -> str:
    m = re.match(r"(\d{4}-\d{2}-\d{2})-daily-brief\.md$", post_path.name)
    if not m:
        raise ValueError(f"Unexpected post filename: {post_path.name}")
    return m.group(1)


def load_manifest(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def generate_one(post_path: Path, audio_dir: Path, manifest: dict, args):
    date = post_date(post_path)
    if date in manifest and not args.force:
        print(f"SKIP {date}: audio already published at {manifest[date]}")
        return False

    final_path = audio_dir / f"{date}-daily-brief.mp3"
    if final_path.exists() and not args.force:
        print(f"SKIP {date}: local {final_path} already exists")
        return False

    spoken = markdown_to_spoken_text(post_path.read_text(encoding="utf-8"))
    if args.normalized_text_out:
        preview = Path(args.normalized_text_out)
        preview.parent.mkdir(parents=True, exist_ok=True)
        preview.write_text(spoken + "\n", encoding="utf-8")
        print(f"Normalized TTS text: {preview}")

    chunks = split_text(spoken, args.max_chars)
    if not chunks:
        raise RuntimeError(f"No speakable text found in {post_path}")

    print(f"{date}: {len(spoken)} normalized chars -> {len(chunks)} chunks")
    audio_dir.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix=f"tts-{date}-") as td:
        tmp = Path(td)
        parts = []
        for i, chunk in enumerate(chunks, 1):
            part = tmp / f"part-{i:03d}.mp3"
            print(f"  TTS {i}/{len(chunks)} ({len(chunk)} chars)")
            synthesize_chunk(chunk, part, args.voice, args.speed, args.volume, args.pitch, args.url)
            parts.append(part)
        concat_mp3(parts, final_path)

    print(f"OK: {final_path} ({final_path.stat().st_size} bytes)")
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--posts-dir", default="_posts")
    ap.add_argument("--audio-dir", default=".tts-audio")
    ap.add_argument("--manifest", default="_data/audio.json")
    ap.add_argument("--post", help="Generate one specific Markdown post")
    ap.add_argument("--all-missing", action="store_true")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--normalized-text-out", help="Optional path to save the exact normalized text sent to TTS")
    ap.add_argument("--max-chars", type=int, default=MAX_CHARS)
    ap.add_argument("--url", default=DEFAULT_URL)
    ap.add_argument("--voice", default=DEFAULT_VOICE)
    ap.add_argument("--speed", type=int, default=50)
    ap.add_argument("--volume", type=int, default=52)
    ap.add_argument("--pitch", type=int, default=50)
    args = ap.parse_args()

    posts_dir = Path(args.posts_dir)
    audio_dir = Path(args.audio_dir)
    manifest = load_manifest(Path(args.manifest))
    if args.post:
        posts = [Path(args.post)]
    else:
        posts = sorted(posts_dir.glob("*-daily-brief.md"))
        if not args.all_missing and posts:
            posts = [posts[-1]]

    if not posts:
        print("No Daily Brief posts found")
        return

    generated = 0
    for post in posts:
        if generate_one(post, audio_dir, manifest, args):
            generated += 1
    print(f"Generated {generated} audio file(s)")


if __name__ == "__main__":
    main()

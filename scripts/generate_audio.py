# -*- coding: utf-8 -*-
import argparse
import html
import re
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

from xfyun_tts import DEFAULT_URL, DEFAULT_VOICE, run_once


MAX_CHARS = 1800


def strip_front_matter(text: str) -> str:
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            return parts[2].lstrip()
    return text


def markdown_to_spoken_text(markdown: str) -> str:
    text = strip_front_matter(markdown)

    # Remove fenced code blocks and raw HTML tags.
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text)

    # Images are not useful in audio. Keep link labels but drop URLs.
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"https?://\S+", "", text)

    # Markdown syntax -> readable punctuation.
    text = re.sub(r"^#{1,6}\s*", "", text, flags=re.M)
    text = re.sub(r"^>\s?", "", text, flags=re.M)
    text = re.sub(r"^[-*+]\s+", "", text, flags=re.M)
    text = re.sub(r"^\s*\d+\.\s+", "", text, flags=re.M)
    text = text.replace("**", "").replace("__", "").replace("`", "")
    text = html.unescape(text)

    # Make a few recurring financial forms friendlier to Chinese TTS.
    text = re.sub(r"(\d+(?:\.\d+)?)\s*bp\b", r"\1 个基点", text, flags=re.I)
    text = re.sub(r"(\d+(?:\.\d+)?)\s*%", r"\1%", text)
    text = re.sub(r"\b2Y\b", "两年期", text)
    text = re.sub(r"\b10Y\b", "十年期", text)
    text = re.sub(r"\b30Y\b", "三十年期", text)

    # Preserve paragraph pauses but normalize whitespace inside each paragraph.
    paragraphs = []
    for p in re.split(r"\n\s*\n", text):
        p = re.sub(r"\s+", " ", p).strip()
        if p:
            paragraphs.append(p)
    return "\n\n".join(paragraphs)


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
        # Split at sentence boundaries first; long sentences get a punctuation-aware fallback.
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
    subprocess.run(
        ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0",
         "-i", str(list_file), "-c", "copy", str(out_path)],
        check=True,
    )


def post_date(post_path: Path) -> str:
    m = re.match(r"(\d{4}-\d{2}-\d{2})-daily-brief\.md$", post_path.name)
    if not m:
        raise ValueError(f"Unexpected post filename: {post_path.name}")
    return m.group(1)


def generate_one(post_path: Path, audio_dir: Path, args):
    date = post_date(post_path)
    final_path = audio_dir / f"{date}-daily-brief.mp3"
    if final_path.exists() and not args.force:
        print(f"SKIP {date}: {final_path} already exists")
        return False

    spoken = markdown_to_spoken_text(post_path.read_text(encoding="utf-8"))
    chunks = split_text(spoken, args.max_chars)
    if not chunks:
        raise RuntimeError(f"No speakable text found in {post_path}")

    print(f"{date}: {len(spoken)} chars -> {len(chunks)} chunks")
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
    ap.add_argument("--audio-dir", default="audio")
    ap.add_argument("--post", help="Generate one specific Markdown post")
    ap.add_argument("--all-missing", action="store_true", help="Generate every post whose MP3 is missing")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--max-chars", type=int, default=MAX_CHARS)
    ap.add_argument("--url", default=DEFAULT_URL)
    ap.add_argument("--voice", default=DEFAULT_VOICE)
    ap.add_argument("--speed", type=int, default=50)
    ap.add_argument("--volume", type=int, default=52)
    ap.add_argument("--pitch", type=int, default=50)
    args = ap.parse_args()

    posts_dir = Path(args.posts_dir)
    audio_dir = Path(args.audio_dir)
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
        if generate_one(post, audio_dir, args):
            generated += 1
    print(f"Generated {generated} audio file(s)")


if __name__ == "__main__":
    main()

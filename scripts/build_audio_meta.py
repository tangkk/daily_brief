# -*- coding: utf-8 -*-
import json
import subprocess
import urllib.request
from pathlib import Path

MANIFEST = Path('_data/audio.json')
META = Path('_data/audio_meta.json')


def content_length(url: str) -> int:
    req = urllib.request.Request(url, method='HEAD', headers={'User-Agent': 'lobster-daily-rss-builder/1.0'})
    with urllib.request.urlopen(req, timeout=20) as resp:
        value = resp.headers.get('Content-Length')
        if not value:
            raise RuntimeError(f'Missing Content-Length for {url}')
        size = int(value)
        if size <= 0:
            raise RuntimeError(f'Invalid Content-Length for {url}: {value}')
        return size


def duration_seconds(url: str) -> int:
    proc = subprocess.run(
        [
            'ffprobe', '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            url,
        ],
        check=True,
        capture_output=True,
        text=True,
        timeout=60,
    )
    seconds = int(round(float(proc.stdout.strip())))
    if seconds <= 0:
        raise RuntimeError(f'Invalid duration for {url}: {proc.stdout!r}')
    return seconds


def format_duration(seconds: int) -> str:
    hours, rem = divmod(seconds, 3600)
    minutes, secs = divmod(rem, 60)
    return f'{hours:02d}:{minutes:02d}:{secs:02d}'


def main():
    audio = json.loads(MANIFEST.read_text(encoding='utf-8'))
    meta = {}
    for date, url in sorted(audio.items()):
        size = content_length(url)
        seconds = duration_seconds(url)
        duration = format_duration(seconds)
        meta[date] = {
            'length': size,
            'duration': duration,
            'duration_seconds': seconds,
        }
        print(f'{date}: {size} bytes, {duration}')
    META.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()

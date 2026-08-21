# -*- coding: utf-8 -*-
import json
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


def main():
    audio = json.loads(MANIFEST.read_text(encoding='utf-8'))
    meta = {}
    for date, url in sorted(audio.items()):
        size = content_length(url)
        meta[date] = {'length': size}
        print(f'{date}: {size} bytes')
    META.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()

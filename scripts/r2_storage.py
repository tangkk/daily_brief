# -*- coding: utf-8 -*-
import argparse
import json
import os
import re
from pathlib import Path

import boto3


def required_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def r2_client():
    return boto3.client(
        "s3",
        endpoint_url=required_env("R2_ENDPOINT").rstrip("/"),
        aws_access_key_id=required_env("R2_ACCESS_KEY_ID"),
        aws_secret_access_key=required_env("R2_SECRET_ACCESS_KEY"),
        region_name="auto",
    )


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(dict(sorted(data.items())), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def date_from_audio(path: Path) -> str:
    m = re.match(r"(\d{4}-\d{2}-\d{2})-daily-brief\.mp3$", path.name)
    if not m:
        raise ValueError(f"Unexpected audio filename: {path.name}")
    return m.group(1)


def object_key(date: str) -> str:
    year, month, _ = date.split("-")
    return f"audio/{year}/{month}/{date}-daily-brief.mp3"


def public_url(date: str) -> str:
    base = required_env("R2_PUBLIC_BASE_URL").rstrip("/")
    return f"{base}/{object_key(date)}"


def upload_file(client, bucket: str, path: Path, date: str):
    key = object_key(date)
    print(f"UPLOAD {path} -> s3://{bucket}/{key}")
    client.upload_file(
        str(path),
        bucket,
        key,
        ExtraArgs={
            "ContentType": "audio/mpeg",
            "CacheControl": "public, max-age=31536000, immutable",
        },
    )
    head = client.head_object(Bucket=bucket, Key=key)
    size = int(head.get("ContentLength", 0))
    if size <= 0:
        raise RuntimeError(f"Uploaded object has invalid size: {key}")
    print(f"OK {key} ({size} bytes)")
    return public_url(date), size


def sync_local(audio_dir: Path, manifest_path: Path, metadata_path: Path):
    client = r2_client()
    bucket = required_env("R2_BUCKET")
    manifest = load_json(manifest_path)
    metadata = load_json(metadata_path)
    changed = False

    if not audio_dir.exists():
        print(f"No local audio directory: {audio_dir}")
        return False

    for path in sorted(audio_dir.glob("*-daily-brief.mp3")):
        date = date_from_audio(path)
        url, size = upload_file(client, bucket, path, date)
        if manifest.get(date) != url:
            manifest[date] = url
            changed = True

        meta = {"length": size, "type": "audio/mpeg"}
        hash_path = path.with_suffix(".sha256")
        if hash_path.exists():
            source_sha256 = hash_path.read_text(encoding="utf-8").strip()
            if source_sha256:
                meta["source_sha256"] = source_sha256

        if metadata.get(date) != meta:
            metadata[date] = meta
            changed = True

    if changed:
        save_json(manifest_path, manifest)
        save_json(metadata_path, metadata)
    return changed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--audio-dir", default="audio")
    ap.add_argument("--manifest", default="_data/audio.json")
    ap.add_argument("--metadata", default="_data/audio_meta.json")
    args = ap.parse_args()
    sync_local(Path(args.audio_dir), Path(args.manifest), Path(args.metadata))


if __name__ == "__main__":
    main()

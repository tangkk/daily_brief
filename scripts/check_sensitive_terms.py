#!/usr/bin/env python3
import argparse, json
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("text_file")
    ap.add_argument("--terms", default=None)
    args = ap.parse_args()

    base = Path(__file__).resolve().parent
    terms_path = Path(args.terms) if args.terms else base / "sensitive_terms.json"
    text = Path(args.text_file).read_text(encoding="utf-8")
    terms = json.loads(terms_path.read_text(encoding="utf-8")).get("blocked_terms", [])
    hits = [str(term) for term in terms if str(term) and str(term) in text]
    if hits:
        print(f"Sensitive terms detected in written Daily Brief: {len(hits)} configured term(s) matched")
        raise SystemExit(2)
    print("Written sensitive-term check passed")


if __name__ == "__main__":
    main()

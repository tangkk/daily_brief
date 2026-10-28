#!/usr/bin/env python3
"""龙虾压力指数 (Lobster Stress Index).

For each US business day, eight market indicators are ranked against their own
trailing 252-business-day window (percentile, 0-100), oriented so that higher
means more market stress, and averaged. 50 is the past year's normal level.

Usage:
  python scripts/stress_index.py                    # refresh _data/stress_index.json
  python scripts/stress_index.py --edition 2026-10-29
      # also write handoffs/2026-10-29-stress.json with the reading for that
      # edition (latest market date strictly before the edition date)

Data: Yahoo Finance daily closes (CSI 300 via the 510300 ETF, high-yield
credit via the HYG ETF). Standard library only. On any fetch failure it exits non-zero and leaves
existing files untouched, so a failed run never corrupts the archive.
"""
import argparse, datetime as dt, json, sys, time, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "_data" / "stress_index.json"
WINDOW, MIN_OBS, FFILL_LIMIT, MIN_COMPONENTS = 252, 200, 10, 6
HISTORY_START = dt.date(2025, 1, 1)
UA = "lobster-daily-stress-index/1.0 (+https://tangkk.github.io/daily_brief/)"

# key, label, source, id, stress_when_high
COMPONENTS = [
    ("ust10y", "十年期美债收益率", "yahoo", "^TNX", True),
    ("move", "MOVE 债市波动", "yahoo", "^MOVE", True),
    ("vix", "VIX 股市波动", "yahoo", "^VIX", True),
    ("hy", "高收益债（HYG）", "yahoo", "HYG", False),  # HY bond ETF price; falls under credit stress
    ("brent", "布伦特原油", "yahoo", "BZ=F", True),
    ("dxy", "美元指数", "yahoo", "DX-Y.NYB", True),
    ("sox", "费城半导体指数", "yahoo", "^SOX", False),
    ("csi300", "沪深 300", "yahoo", "510300.SS", False),  # CSI 300 ETF as index proxy
]


def get(url):
    last = None
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=40) as r:
                return r.read().decode("utf-8")
        except Exception as e:  # retry transient network errors
            last = e
            time.sleep(10 * (attempt + 1))  # back off on rate limits
    raise last


def fetch_yahoo(sym):
    q = urllib.request.quote(sym, safe="")
    j = json.loads(get(f"https://query1.finance.yahoo.com/v8/finance/chart/{q}?range=5y&interval=1d"))
    res = j["chart"]["result"][0]
    off = res["meta"].get("gmtoffset", 0)
    out = {}
    for t, c in zip(res["timestamp"], res["indicators"]["quote"][0]["close"]):
        if c is not None:
            out[dt.datetime.fromtimestamp(t + off, dt.timezone.utc).date()] = float(c)
    return out


def bdays(start, end):
    d = start
    while d <= end:
        if d.weekday() < 5:
            yield d
        d += dt.timedelta(days=1)


def aligned(series, cal):
    """Forward-fill onto the business-day calendar, at most FFILL_LIMIT days."""
    out, last, age = [], None, 0
    for d in cal:
        if d in series:
            last, age = series[d], 0
        elif last is not None:
            age += 1
        out.append(last if last is not None and age <= FFILL_LIMIT else None)
    return out


def percentile_series(vals):
    out = []
    for i, v in enumerate(vals):
        win = [x for x in vals[max(0, i - WINDOW + 1): i + 1] if x is not None]
        if v is None or len(win) < MIN_OBS:
            out.append(None)
        else:
            out.append(100.0 * sum(1 for x in win if x <= v) / len(win))
    return out


def compute(end):
    start = end - dt.timedelta(days=3 * 366)
    raw = {}
    for key, _, src, sid, _ in COMPONENTS:
        raw[key] = fetch_yahoo(sid)
        time.sleep(1)
        if not raw[key]:
            raise RuntimeError(f"no data for {key}")
    cal = list(bdays(start, end))
    pct = {}
    for key, _, _, _, high in COMPONENTS:
        p = percentile_series(aligned(raw[key], cal))
        pct[key] = [None if x is None else (x if high else 100 - x) for x in p]
    rows = []
    for i, d in enumerate(cal):
        if d < HISTORY_START:
            continue
        comps = [pct[k][i] for k, *_ in COMPONENTS]
        have = [c for c in comps if c is not None]
        if len(have) >= MIN_COMPONENTS:
            rows.append({"date": d.isoformat(), "index": round(sum(have) / len(have), 1),
                         "c": [None if c is None else round(c) for c in comps]})
    if not rows:
        raise RuntimeError("no computable rows")
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--edition", help="Asia/Shanghai edition date YYYY-MM-DD")
    a = ap.parse_args()
    edition = dt.date.fromisoformat(a.edition) if a.edition else None
    end = (edition - dt.timedelta(days=1)) if edition else dt.date.today()
    try:
        rows = compute(end)
    except Exception as e:  # leave existing files untouched
        print(f"Stress index not updated: {e}", file=sys.stderr)
        return 2
    doc = {
        "name": "龙虾压力指数",
        "method": "8 个市场指标在过去 252 个交易日中的百分位（按压力方向）取平均；50 = 过去一年的正常水平，越高越紧张。",
        "components": [{"key": k, "label": l, "stress_when_high": h} for k, l, _, _, h in COMPONENTS],
        "updated": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "series": rows,
    }
    DATA.write_text(json.dumps(doc, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    last, prev = rows[-1], rows[-2] if len(rows) > 1 else None
    labels = [l for _, l, *_ in COMPONENTS]
    top = sorted(((c, labels[i]) for i, c in enumerate(last["c"]) if c is not None), reverse=True)[:3]
    summary = {"market_date": last["date"], "index": last["index"],
               "prev_date": prev and prev["date"], "prev_index": prev and prev["index"],
               "change": prev and round(last["index"] - prev["index"], 1),
               "top_components": [{"label": l, "percentile": c} for c, l in top]}
    print(json.dumps(summary, ensure_ascii=False))
    if edition:
        out = ROOT / "handoffs" / f"{edition.isoformat()}-stress.json"
        out.write_text(json.dumps(summary, ensure_ascii=False) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

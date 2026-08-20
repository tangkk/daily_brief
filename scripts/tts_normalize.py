# -*- coding: utf-8 -*-
"""Deterministic Chinese TTS normalization for Daily Brief spoken scripts.

The GitHub-visible spoken script remains readable Markdown. Only transient text
sent to XFYUN is normalized here. Keep this module deterministic and covered by
regression tests: audio generation must fail before TTS if these rules regress.
"""
import re
from decimal import Decimal, InvalidOperation

DIGITS = "零一二三四五六七八九"
SMALL_UNITS = ("", "十", "百", "千")
BIG_UNITS = ("", "万", "亿", "万亿")

TERM_MAP = {
    "forward P/E": "预期市盈率", "BTC ETF": "比特币现货ETF", "funding rate": "资金费率",
    "open interest": "未平仓合约", "private credit": "私募信贷", "data center": "数据中心",
    "Data center": "数据中心", "risk-on": "风险偏好上升", "risk-off": "避险",
    "ETH/BTC": "以太坊兑比特币", "USD/CNY": "美元兑在岸人民币", "USD/CNH": "美元兑离岸人民币",
    "FOMC": "美联储公开市场委员会", "SLOOS": "银行信贷员调查", "Hyperscaler": "大型云厂商",
    "hyperscaler": "大型云厂商", "stablecoin": "稳定币", "Stablecoin": "稳定币",
    "utilization": "利用率", "financing": "融资", "power": "电力", "grid": "电网",
    "Brent": "布伦特原油", "Nvidia": "英伟达", "NVIDIA": "英伟达", "Nasdaq": "纳斯达克",
    "BESIII": "北京谱仪三号", "DXY": "美元指数", "CNY": "在岸人民币", "CNH": "离岸人民币",
    "RMB": "人民币", "BTC": "比特币", "ETH": "以太坊", "ETF": "交易所交易基金",
    "Fed": "美联储", "FED": "美联储", "AI": "人工智能", "LLM": "大语言模型", "LLMs": "大语言模型",
    "GPU": "图形处理器", "GPUs": "图形处理器", "CapEx": "资本开支", "CAPEX": "资本开支",
    "Opex": "运营开支", "OPEX": "运营开支", "FCF": "自由现金流", "ROI": "投资回报率",
    "ARPU": "每用户平均收入", "EPS": "每股收益", "P/E": "市盈率", "PMI": "采购经理指数",
    "ISM": "供应管理协会指数", "CPI": "消费者价格指数", "PPI": "生产者价格指数",
    "PCE": "个人消费支出价格指数", "GDP": "国内生产总值", "OAS": "期权调整利差",
    "HY": "高收益债", "CRE": "商业地产", "QE": "量化宽松", "YCC": "收益率曲线控制",
    "YoY": "同比", "y/y": "同比", "MoM": "环比", "m/m": "环比", "QoQ": "环比", "q/q": "环比",
    "SOX": "费城半导体指数",
}


def _group_to_cn(n: int) -> str:
    if n == 0: return ""
    out, zero_pending = [], False
    for pos in range(3, -1, -1):
        divisor = 10 ** pos; d = n // divisor; n %= divisor
        if d:
            if zero_pending and out: out.append("零")
            if not (d == 1 and pos == 1 and not out): out.append(DIGITS[d])
            out.append(SMALL_UNITS[pos]); zero_pending = False
        elif out and n: zero_pending = True
    return "".join(out)


def int_to_cn(n: int) -> str:
    if n == 0: return "零"
    if n < 0: return "负" + int_to_cn(-n)
    groups = []
    while n: groups.append(n % 10000); n //= 10000
    out, zero_between = [], False
    for idx in range(len(groups) - 1, -1, -1):
        g = groups[idx]
        if not g:
            if out: zero_between = True
            continue
        if out and (zero_between or g < 1000) and out[-1] != "零": out.append("零")
        out.append(_group_to_cn(g))
        if idx < len(BIG_UNITS): out.append(BIG_UNITS[idx])
        zero_between = False
    return "".join(out).rstrip("零")


def number_to_cn(raw: str) -> str:
    raw = str(raw).replace(",", "").strip()
    try: d = Decimal(raw)
    except InvalidOperation: return raw
    sign = "负" if d < 0 else ""; raw_abs = format(abs(d), "f")
    if "." not in raw_abs: return sign + int_to_cn(int(raw_abs))
    integer, frac = raw_abs.split(".", 1); frac = frac.rstrip("0")
    if not frac: return sign + int_to_cn(int(integer))
    return sign + int_to_cn(int(integer)) + "点" + "".join(DIGITS[int(x)] for x in frac)


def _scaled_cn(raw: str, multiplier: str) -> str:
    try: value = Decimal(raw.replace(",", "")) * Decimal(multiplier)
    except InvalidOperation: return raw
    return number_to_cn(format(value, "f"))


def _signed_word(sign: str) -> str: return "上升" if sign in ("+", "＋") else "下降"


def _normalize_contextual_changes(text: str) -> str:
    text = re.sub(r"(上涨|上升|增长|增加|升高|走高|反弹)\s*[+＋]?\s*(\d[\d,]*(?:\.\d+)?)\s*%", lambda m: f"{m.group(1)}百分之{number_to_cn(m.group(2))}", text)
    text = re.sub(r"(下跌|下降|减少|降低|走低|收缩|回落)\s*[-−]?\s*(\d[\d,]*(?:\.\d+)?)\s*%", lambda m: f"{m.group(1)}百分之{number_to_cn(m.group(2))}", text)
    text = re.sub(r"(上涨|上升|增长|增加|升高|走高|反弹)\s*[+＋]?\s*(\d[\d,]*(?:\.\d+)?)\s*(?:bp|bps|个基点)", lambda m: f"{m.group(1)}{number_to_cn(m.group(2))}个基点", text, flags=re.I)
    text = re.sub(r"(下跌|下降|减少|降低|走低|收缩|回落)\s*[-−]?\s*(\d[\d,]*(?:\.\d+)?)\s*(?:bp|bps|个基点)", lambda m: f"{m.group(1)}{number_to_cn(m.group(2))}个基点", text, flags=re.I)
    return text


def _normalize_ranges(text: str) -> str:
    text = re.sub(r"(\d[\d,]*(?:\.\d+)?)\s*%\s*[–—~-]\s*(\d[\d,]*(?:\.\d+)?)\s*%", lambda m: f"百分之{number_to_cn(m.group(1))}到百分之{number_to_cn(m.group(2))}", text)
    text = re.sub(r"(\d[\d,]*(?:\.\d+)?)\s*(?:bp|bps)\s*[–—~-]\s*(\d[\d,]*(?:\.\d+)?)\s*(?:bp|bps)", lambda m: f"{number_to_cn(m.group(1))}到{number_to_cn(m.group(2))}个基点", text, flags=re.I)
    return text


def _normalize_money(text: str) -> str:
    text = re.sub(r"\$\s*(\d[\d,]*(?:\.\d+)?)\s*/\s*oz\b", lambda m: f"每盎司{number_to_cn(m.group(1))}美元", text, flags=re.I)
    text = re.sub(r"\$\s*(\d[\d,]*(?:\.\d+)?)\s*万亿", lambda m: f"{number_to_cn(m.group(1))}万亿美元", text)
    text = re.sub(r"\$\s*(\d[\d,]*(?:\.\d+)?)\s*亿", lambda m: f"{number_to_cn(m.group(1))}亿美元", text)
    text = re.sub(r"\$\s*(\d[\d,]*(?:\.\d+)?)\s*(trillion|tn)\b", lambda m: f"{number_to_cn(m.group(1))}万亿美元", text, flags=re.I)
    text = re.sub(r"\$\s*(\d[\d,]*(?:\.\d+)?)\s*(billion|bn)\b", lambda m: f"{_scaled_cn(m.group(1), '10')}亿美元", text, flags=re.I)
    text = re.sub(r"\$\s*(\d[\d,]*(?:\.\d+)?)\s*(million|mn)\b", lambda m: f"{_scaled_cn(m.group(1), '100')}万美元", text, flags=re.I)
    text = re.sub(r"\$\s*(\d[\d,]*(?:\.\d+)?)", lambda m: f"{number_to_cn(m.group(1))}美元", text)
    return text


def _normalize_units(text: str) -> str:
    text = re.sub(r"\b10Y\s*[–—-]\s*2Y\b", "十年期与两年期美债利差", text, flags=re.I)
    text = re.sub(r"\b(2|5|10|20|30)Y\b", lambda m: f"{number_to_cn(m.group(1))}年期", text, flags=re.I)
    text = _normalize_ranges(text); text = _normalize_contextual_changes(text)
    text = re.sub(r"([+＋\-−])\s*(\d[\d,]*(?:\.\d+)?)\s*%", lambda m: f"{_signed_word(m.group(1))}百分之{number_to_cn(m.group(2))}", text)
    text = re.sub(r"([+＋\-−])\s*(\d[\d,]*(?:\.\d+)?)\s*(?:bp|bps)\b", lambda m: f"{_signed_word(m.group(1))}{number_to_cn(m.group(2))}个基点", text, flags=re.I)
    text = re.sub(r"(?<![\w.])(\d[\d,]*(?:\.\d+)?)\s*%", lambda m: f"百分之{number_to_cn(m.group(1))}", text)
    text = re.sub(r"(?<![\w.])(\d[\d,]*(?:\.\d+)?)\s*(?:bp|bps)\b", lambda m: f"{number_to_cn(m.group(1))}个基点", text, flags=re.I)
    for unit in ("万亿", "百万", "十亿", "亿", "万", "千"):
        text = re.sub(rf"(?<!\w)(\d[\d,]*(?:\.\d+)?)\s*{unit}", lambda m, u=unit: f"{number_to_cn(m.group(1))}{u}", text)
    text = re.sub(r"(?<!\w)(\d[\d,]*(?:\.\d+)?)\s*倍", lambda m: f"{number_to_cn(m.group(1))}倍", text)
    return text


def _normalize_dates(text: str) -> str:
    return re.sub(r"(?<!\d)(20\d{2})-(\d{1,2})-(\d{1,2})(?!\d)", lambda m: f"{''.join(DIGITS[int(x)] for x in m.group(1))}年{number_to_cn(m.group(2))}月{number_to_cn(m.group(3))}日", text)


def _replace_terms(text: str) -> str:
    for src in sorted(TERM_MAP, key=len, reverse=True):
        dst = TERM_MAP[src]
        if re.fullmatch(r"[A-Za-z]+", src): text = re.sub(rf"(?<![A-Za-z]){re.escape(src)}(?![A-Za-z])", dst, text)
        else: text = text.replace(src, dst)
    return text


def normalize_for_tts(text: str) -> str:
    text = text.replace("→", "，然后是").replace("↑", "上升").replace("↓", "下降")
    text = text.replace("≈", "约").replace("~", "约").replace("&", "和")
    text = _normalize_dates(text); text = _normalize_money(text); text = _normalize_units(text); text = _replace_terms(text)
    text = re.sub(r"\s*/\s*", "和", text); text = re.sub(r"\s*[|｜]\s*", "，", text); text = re.sub(r"\s*[–—]\s*", "到", text)
    text = text.replace("%", "百分号"); text = re.sub(r"\b(?:bp|bps)\b", "基点", text, flags=re.I)
    text = re.sub(r"[\t ]+", " ", text); text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"\s+([，。！？；：])", r"\1", text); text = re.sub(r"([，。！？；：])\s+", r"\1", text)
    text = re.sub(r"(?<=[\u4e00-\u9fff]) (?=[\u4e00-\u9fff])", "", text)
    return text.strip()

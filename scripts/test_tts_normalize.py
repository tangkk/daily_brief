# -*- coding: utf-8 -*-
from tts_normalize import normalize_for_tts, number_to_cn


def check(src, expected):
    got = normalize_for_tts(src)
    assert got == expected, f"\nSRC: {src}\nGOT: {got}\nEXP: {expected}"


def main():
    assert number_to_cn("0") == "零"
    assert number_to_cn("4.18") == "四点一八"
    assert number_to_cn("4500") == "四千五百"
    assert number_to_cn("40000") == "四万"
    assert number_to_cn("3400") == "三千四百"

    check("2Y 4.18%，10Y 4.66%，30Y 5.20%。",
          "二年期百分之四点一八，十年期百分之四点六六，三十年期百分之五点二。")
    check("10Y–2Y约+47bp。", "十年期与两年期美债利差约上升四十七个基点。")
    check("30Y下降9bp。", "三十年期下降九个基点。")
    check("零售销售-0.6%，工业生产+4.5%。", "零售销售下降百分之零点六，工业生产上升百分之四点五。")
    check("CPI下降0.6%，PPI增长3.5%。", "消费者价格指数下降百分之零点六，生产者价格指数增长百分之三点五。")
    check("收益率5.18%–5.20%。", "收益率百分之五点一八到百分之五点二。")
    check("黄金约$4,500/oz。", "黄金约每盎司四千五百美元。")
    check("融资规模$500bn。", "融资规模五千亿美元。")
    check("项目融资$3bn，另一笔$25mn。", "项目融资三十亿美元，另一笔二千五百万美元。")
    check("BTC ETF流入，stablecoin供应增长。", "比特币现货交易所交易基金流入，稳定币供应增长。")
    check("DXY下降，USD/CNY走高，USD/CNH走低。", "美元指数下降，美元兑在岸人民币走高，美元兑离岸人民币走低。")
    check("ETH/BTC仍低，FCF和ROI更重要。", "以太坊兑比特币仍低，自由现金流和投资回报率更重要。")
    check("AI CapEx → power → grid → utilization / FCF。",
          "人工智能资本开支，然后是电力，然后是电网，然后是利用率和自由现金流。")
    check("Nvidia的数据中心financing扩大。", "英伟达的数据中心融资扩大。")
    check("2026-08-21开始。", "二零二六年八月二十一日开始。")
    check("forward P/E约20倍。", "预期市盈率约二十倍。")
    check("PMI、CPI、PPI、PCE、GDP。",
          "采购经理指数、消费者价格指数、生产者价格指数、个人消费支出价格指数、国内生产总值。")
    check("QE不是YCC。", "量化宽松不是收益率曲线控制。")
    check("Brent上涨6%，Nasdaq下跌2%。", "布伦特原油上涨百分之六，纳斯达克下跌百分之二。")

    sample = "30Y收益率从5.34%降至5.20%，约-14bp；DXY跌破99，BTC反弹6%，ETH/BTC仍低。"
    out = normalize_for_tts(sample)
    assert "%" not in out
    assert "bp" not in out.lower()
    assert "30Y" not in out
    assert "DXY" not in out
    assert "BTC" not in out
    assert "ETH/BTC" not in out

    print("TTS normalization regression tests passed")


if __name__ == "__main__":
    main()

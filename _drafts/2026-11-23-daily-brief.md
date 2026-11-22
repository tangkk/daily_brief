---
layout: daily_brief
title: "2026-11-23"
date: 2026-11-23 07:00:00 +0800
headline: "黎曼猜想形式证明获核验；AI 服务器报价最高上调 45%"
---

Lean 与 Mathlib 社群核验了 Levent Alpöge 借助 Claude 完成的黎曼猜想形式化证明。金融时报报道多家服务器供应商要求提高部分已签约 AI 设备的交付价格；联合国气候会议在核心决定上未达成一致。技术能力、算力成本与能源转型的进展，今天呈现出不同的证据层次。[Lean 社群声明](https://leanprover-community.github.io/blog/posts/riemann-hypothesis/) · [金融时报](https://www.ft.com/content/dd2a6594-6146-4ff1-ac8e-54749c1fc99f) · [联合国气候秘书处](https://unfccc.int/news/un-climate-change-executive-secretary-simon-stiell-remarks-at-the-closing-plenary-of-cop31)

## Number of the Day / 今日数字

**45%**：金融时报报道的部分英伟达 AI 服务器交付前提价幅度上限，涉及此前已谈妥价格的订单。报道没有证明所有客户都按这一幅度付款；实际合同成本仍须看交付和发票。[金融时报](https://www.ft.com/content/dd2a6594-6146-4ff1-ac8e-54749c1fc99f)

## Top Headlines

### 1. Lean 与 Mathlib 社群核验黎曼猜想形式化证明

Levent Alpöge 十一月二十日发布借助 Claude 完成、约 **1700 万行 Lean 代码**的黎曼猜想证明。Lean 与 Mathlib 社群二十一日发表联合声明，称已核对命题表述、证明依赖和形式化检查结果，并认可这份证明的正确性。这个进展把 AI 辅助的数学发现从研究者主张推进到独立形式化核验；人类可阅读的完整论证仍在整理，数学界对方法的理解还需要时间。黎曼猜想涉及素数分布，是数学领域长期未解的问题。[Lean 与 Mathlib 联合声明](https://leanprover-community.github.io/blog/posts/riemann-hypothesis/) · [滑铁卢大学讲解稿](https://www.math.uwaterloo.ca/~mrubinst/alpoge_claude_grh/zeta-paper.pdf)

### 2. 金融时报：AI 服务器供应商要求部分客户接受最高 45% 提价

金融时报二十二日报道，戴尔、慧与、联想和超微电脑等供应商，在部分英伟达服务器交付前，要求客户支付高于数月前约定的价格；一名知情人士称涨幅可达 **25%、30% 或 45%**。报道指内存等零部件成本上升，部分大型交易公司受到影响。报道尚未证实所有合同是否允许交付前调价，也未给出各家公司的实际成交规模。这是一项有明确出处的供应链价格风险；若成本向下游传递，数据中心资本预算和投资回收期可能需要重算。[金融时报原报道](https://www.ft.com/content/dd2a6594-6146-4ff1-ac8e-54749c1fc99f)

### 3. COP31 闭幕，核心气候决定未获一致同意

联合国气候变化秘书处二十二日确认，安塔利亚 COP31 未能就由大会主席方主导的两项核心决定达成一致。会议仍就公正转型等议题作出决定，但化石能源相关争议阻碍了整体协议。对能源企业和投资者而言，未来的电力、减排和融资规则仍须观察各国具体行动。会议未达成总协议，并不意味着各国既有目标或已生效政策自动失效。[联合国气候秘书处闭幕声明](https://unfccc.int/news/un-climate-change-executive-secretary-simon-stiell-remarks-at-the-closing-plenary-of-cop31) · [美联社现场报道](https://apnews.com/article/f6e36c4caf13ec6fed57c9f077cbd067)

### 4. Thinking Machines 开放 264 亿参数循环模型权重

Thinking Machines Lab 二十日发布 **Inkling 2 Mini**，采用混合专家架构，共 **264 亿参数**、每个 token 激活约 **34 亿参数**，循环计算使实际权重访问约 **54 亿参数**。公司称模型权重占用约 **20GB**，可在本地设备运行，并以开放权重提供推理和定制；其公布的 DeepSWE v1.1 与 Vals Index v2.2 成绩分别为 **48.2%**、**46.5%**。这些是开发者可复测的模型与基准数据，跨模型的评测设置仍须逐项核对，不能直接推断商业付费需求。[Thinking Machines 技术发布](https://thinkingmachines.ai/news/inkling-2-mini/) · [研究模型卡](https://thinkingmachines.ai/model-card/tml-d24-varloop-research/)

### 5. OpenAI 公布推理提取防护测试，内部攻击成功率降至 0.2%

OpenAI 二十日公布针对对抗性蒸馏的防护更新。其内部自适应黑盒测试中，攻击者提取先前请求受保护推理的平均成功率，从旧版 GPT-6 Astra 的 **54.0%**降至 GPT-6.2 Astra 的 **0.2%**；提取当前请求的对应比例从 **22.9%**降至 **0.9%**。测试汇总六种攻击模型，尚非外部独立审计，也不能覆盖所有攻击方式。公司同时说明在输入、输出和 API 层加入防护；这为模型能力外泄风险提供了可比较的测试口径。[OpenAI 技术说明](https://openai.com/index/combatting-adversarial-distillation/)

### 6. Signal 在移动端限制系统 AI 助手读取聊天画面

Signal 二十日说明，在 **iOS 27** 上默认阻止 Siri AI 对聊天界面截图；在可侦测 AI 助手读取屏幕的 Android 版本上，会自动启用屏幕安全功能。用户可以手动关闭保护。Signal 明确表示这些措施无法覆盖文件系统等其他访问路径，也无法在 macOS 上可靠阻止截图。这是加密通信应用与操作系统级 AI 助手之间新的产品边界，保护范围取决于平台提供的控制接口。[Signal 官方说明](https://signal.org/blog/protecting-your-privacy/) · [Signal 使用说明](https://support.signal.org/hc/en-us/articles/11338514641306-Screen-security-blocking-Siri-AI)

## AI Credit Cycle Pulse / AI 信用周期脉冲

服务器交付前的提价要求若落实，会增加买方算力投入和融资需求；目前仍缺实际成交、项目利润率和客户付费收入的成套数据。供应成本向下游转移的风险，需要与 AI 应用收入分开观察。[金融时报](https://www.ft.com/content/dd2a6594-6146-4ff1-ac8e-54749c1fc99f)

## Compute & Supply-Chain Dashboard / 算力与供应链看板

服务器提价属于据报的合同要求，最高 **45%**，尚无可作为市场统一报价的成交样本。本次没有新的可比 GPU 租赁单价、存储器现货价格或已投运电力数据。[金融时报](https://www.ft.com/content/dd2a6594-6146-4ff1-ac8e-54749c1fc99f)

## AI Applications Watch / AI 应用落地看板

Thinking Machines 开放本地可运行模型，为开发者提供新的部署选择；公司未随发布披露付费用户或收入。Signal 的屏幕保护改变了移动 AI 助手访问应用内容的条件，实际用户影响取决于系统和应用版本。[Thinking Machines](https://thinkingmachines.ai/news/inkling-2-mini/) · [Signal](https://signal.org/blog/protecting-your-privacy/)

## Markets Dashboard

- **龙虾压力指数**：**85.7**，前一交易日重算值 **85.2**，上升 **0.5** 点；主要压力分量来自高收益债 ETF HYG、沪深 300 与 VIX，观测日为十一月二十日。[指数走势](/daily_brief/stress-index/)
- **美国股市**：最近完成的交易日仍为十一月二十日，标普 500 收于 **6910.39** 点、当日跌 **3.7%**；周末没有新的美国股市收盘价。[美联社收盘报道](https://apnews.com/article/c4c3f4878b12989347f8a930ed813dad)

## China Dashboard

此前已生效的先进算力远程使用规则及已报道的晶圆代工订单限制仍需观察许可和实际交付；不能将政策范围直接换算为芯片减产数量。[美国联邦公报](https://www.govinfo.gov/content/pkg/FR-2026-11-19/pdf/2026-23529.pdf) · [路透社报道（Investing.com 转载）](https://www.investing.com/news/stock-market-news/tsmc-tightens-china-ai-chip-curbs-as-new-us-rules-close-manufacturing-loophole-sources-say-5038806)

## AI × Employment Watch

本次发展未提供可比较的 AI 净就业、工时或工资变化数据。模型基准提升和安全功能发布，不能直接作为岗位替代规模的观测值。[Thinking Machines](https://thinkingmachines.ai/news/inkling-2-mini/) · [Signal](https://signal.org/blog/protecting-your-privacy/)

## Science Watch

黎曼猜想的形式化核验是数学研究中的关键新证据。后续重点是可读证明的逐步发表、独立复核具体论证，以及其他研究团队能否复用相关方法。[Lean 与 Mathlib 联合声明](https://leanprover-community.github.io/blog/posts/riemann-hypothesis/) · [滑铁卢大学讲解稿](https://www.math.uwaterloo.ca/~mrubinst/alpoge_claude_grh/zeta-paper.pdf)

## Persistent World State / Bayesian Update

- **科学与模型**：形式化核验提高了 AI 辅助重大数学证明的可信度；模型研究仍需把基准表现与可复现、可解释的学术成果分开衡量。
- **算力经济**：交付前提价报道增加了预算不确定性；供应商要求的价格与买方最终支付的价格尚需区分。
- **能源转型**：COP31 的核心决定未获一致同意，各国具体实施、融资和电力投资路径的重要性上升。

## What to Watch Today

- 跟踪 Lean 证明的可读稿与独立数学评审，以及开放权重模型的外部复测。
- 观察服务器供应商是否确认调价范围、客户是否披露实际支付价格与项目预算变化。
- 核对 COP31 后续正式文件和各国电力、减排政策的实际执行安排。

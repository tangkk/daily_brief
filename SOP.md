# Daily Brief SOP

## Task prompt vs SOP boundary

The repository SOPs are the authoritative source for **what the Daily Brief system does and how it does it**. Scheduled-task prompts are intentionally thin orchestration entrypoints.

- **SOP owns durable behavior:** research scope, source policy, editorial standards, selection/deduplication, Daily/Weekly content contracts, AI Credit Cycle coverage, written/spoken derivation, Podcast-first publication, repository boundaries, checkpoints, recovery, idempotence, rework, and end-to-end verification.
- **Task prompt owns invocation context:** task identity, current-date/timezone interpretation, the Monday–Saturday Daily Brief / Sunday Weekly Review branch, requirement to read both current SOPs before work, and recurring-automation lifecycle guards.
- A task prompt must not duplicate durable business/editorial/publication logic merely as a second copy. If a durable rule changes, update the authoritative SOP rather than maintaining divergent copies in task prompts.
- Normal execution or recovery must not disable, pause, stop, complete, or change the cadence/timezone of the recurring Daily Brief, Weekly Review, or their Watchdogs. Completion refers to the current dated content run, not the recurring automation itself.
- A task may re-enable its paired main schedule if the SOP's recovery contract explicitly requires it, but must not alter unrelated schedules or cross the Mon–Sat/Sunday scope boundary.

The site contains two written content streams with different publishing rules.

## 1. Daily Brief written edition — `tangkk/daily_brief`

- Staged canonical posts: `_drafts/YYYY-MM-DD-daily-brief.md`
- Public canonical posts: `_posts/YYYY-MM-DD-daily-brief.md`
- Layout: `daily_brief`
- Public article title: date only, formatted `YYYY-MM-DD`; do not prefix with `Daily Brief` or `Weekly Review`.
- Public site: https://tangkk.github.io/daily_brief/
- Written RSS: https://tangkk.github.io/daily_brief/feed.xml
- The written site may play the already-published podcast MP3 only from an explicit `_data/audio.json` mapping.
- It never generates TTS, uploads audio, owns podcast metadata, or guesses an R2 URL.

### Daily Brief headline floor

- Every Monday–Saturday written Daily Brief must publish at least **6 distinct, substantive Top Headlines**. Count headline entries, not subparagraphs, dashboards, watchlists, or repeated angles on the same underlying event.
- This is a minimum, not a target ceiling; include more when additional stories independently clear the existing significance, evidence, Information-Gain, safety, and deduplication standards.
- Never pad the list with weak, stale, duplicate, speculative, or low-information material. Continue broad research across relevant beats and source classes until at least six genuinely qualifying stories are found.
- If six qualifying stories cannot be substantiated after a thorough research pass, do not publish an under-six edition or invent filler. Record the shortfall and recovery state internally, keep the written edition staged, and continue/recover research before publication.
- This floor applies to the Monday–Saturday Daily Brief Top Headlines section. The Sunday Weekly Review follows its separate weekly editorial contract and must not be forced into a Daily Brief-style list.

### Source diversity and fair discovery

Source diversity is a mandatory **discovery-stage quality control**, not a publication quota and not a reason to lower evidentiary standards. The goal is to prevent any single publisher, wire service, geography, language, platform, or editorial agenda from determining which developments enter the candidate pool.

1. **Quality remains first.** Rank and publish items by Global Significance, Information Gain, factual support, timeliness, and the existing semantic-deduplication rules. Never include a weaker story merely to satisfy source diversity.
2. **No single-source gatekeeper.** Reuters, Bloomberg, FT, WSJ, AP, BBC, any Chinese outlet, or any other publisher may be an excellent reporting or verification source, but no single outlet may function as the default discovery universe. A development must be able to enter the candidate pool even if that outlet did not cover it.
3. **Diversify before ranking.** Before Top Headlines are selected, actively discover candidates across multiple independent source classes appropriate to the beat: high-quality global wires/general news; specialist financial/business/technology/science reporting; credible regional and local-language reporting; and primary sources such as filings, earnings materials, official statistics, company/research-lab releases, papers, repositories, and conference materials.
4. **Primary sources where they add value.** For company results, financing terms, model/research releases, economic data, regulatory actions, and scientific claims, seek the relevant primary source when reasonably available. Use journalism to supply independent verification, context, consequences, and facts not established by the primary source alone.
5. **Independence matters more than link count.** Syndication, rewrites, and multiple sites carrying the same wire story count as one underlying reporting lineage, not multiple independent confirmations. Prefer genuinely independent reporting or primary evidence when corroboration matters.
6. **Geographic and language fairness.** Discovery should not systematically disadvantage material developments because they originate outside the dominant English-language/global-wire news cycle. Search credible regional/local-language sources where they can materially improve coverage, while applying the same reliability and significance thresholds.
7. **Perspective fairness without false balance.** For disputed or consequential claims, seek materially relevant independent perspectives and evidence. Do not manufacture symmetry between well-supported facts and weak or unsupported claims merely for source balance.
8. **No mechanical outlet quota in the published edition.** It is acceptable for several final items to cite the same outlet when it provides the strongest reporting. Source concentration in the final edition is a diagnostic signal to re-check discovery breadth, not an automatic reason to replace stronger stories with weaker ones.
9. **Internal diversity audit.** Before finalizing candidate selection, check whether the candidate pool is excessively dependent on one publisher or one reporting lineage. If so, perform an additional discovery pass outside that source before ranking. Record this audit internally when practical; never expose source-selection mechanics in reader-facing text or audio.
10. **Fair attribution.** Attribute facts to the source that actually established or reported them, preserve uncertainty, and do not silently convert analysis, anonymous-source reporting, company claims, or third-party estimates into established fact.
11. **Paywalled or access-blocked sources.** Some outlets (for example FT, Reuters, Bloomberg, WSJ) are paywalled or block automated access from the run environment. Do not rely on search snippets alone for material facts from such outlets. Instead, verify against a readable full-text copy, in this order of preference: (a) the primary source itself (company filings and releases, central-bank and statistics-office publications, regulator notices, research-lab posts, open-access papers); (b) a full-text syndicated copy of the same report on an accessible site (for example TradingView or Yahoo Finance carrying Reuters/AP copy); (c) independent accessible reporting that establishes the same facts. Under rule 5, a syndicated copy is the same reporting lineage as the original, not an independent confirmation.
    - Keep attribution with the outlet that established the fact. The citation may link the readable copy, labeled so readers can tell it carries the original outlet's reporting (for example `路透社报道（TradingView 转载）`).
    - If a material fact or exclusive figure is available only as a snippet from a paywalled outlet and cannot be verified through (a)–(c), either attribute it explicitly as that outlet's report and include only what the snippet states, or omit it. Never fill in details that were not actually read.
    - Record access limitations and the readable copies used in the internal run log. Never mention paywalls, access blocks, or this rule in written or spoken content.

Operational order: **broad multi-source discovery → source/lineage check → historical event/thesis match → Information-Gain gate → significance ranking → verification/context enrichment → writing.**

### China AI coverage

China-related AI and technology developments are part of the normal AI news universe and must not be down-ranked, excluded, or omitted merely because they concern China. Apply the same Global Significance Lens, Information-Gain threshold, source quality standards, and semantic-deduplication rules used for comparable AI developments elsewhere.

- Actively consider material developments involving Chinese foundation/model companies, open-source models, training/inference advances, AI products and agents, enterprise and consumer adoption, AI cloud/compute infrastructure, semiconductors and accelerators, financing, revenue/paid demand, and other technically or economically meaningful AI developments.
- China-related AI coverage does not require a dedicated quota and must not be included merely for geographic balance; rank it on substantive importance and information gain.
- Ordinary non-political AI/technology/business reporting is not subject to exclusion merely because the company, research team, product, infrastructure, or market is Chinese.
- Existing China-specific spoken/editorial restrictions continue to govern genuinely political, diplomatic, bilateral, trade-policy, regulatory, or similarly sensitive material. Do not extend those restrictions to ordinary AI/technology coverage by association.
- When a China AI story contains both ordinary technical/business facts and sensitive political/policy material, preserve and evaluate the separable technical/business substance normally where it remains accurate and meaningful on its own.

### Rolling semantic deduplication and Information-Gain gate

Semantic deduplication is a hard selection gate, not a writing-time suggestion. It runs before Top Headlines are ranked.

1. Before candidate selection, read the canonical written editions from the previous 7 days as the strong deduplication window and consult the previous 30 days as the recurrence/thesis-history window. The immediately previous edition has the highest comparison weight, but is never the only baseline.
2. Match candidates at both **event level** and **thesis level**. Different headlines, outlets, URLs, companies, geographies, or wording do not make a story new when the underlying event or editorial conclusion is substantially the same.
3. Any event/thesis seen in the prior 7 days is default-exclude from Top Headlines. It may re-enter only if the new evidence clears a material Information-Gain gate: a new quantitative fact that changes scale, a binding decision, implementation/enforcement, a material verified market reaction, a verified real-world state change, a meaningful reversal, or evidence that materially changes the prior Bayesian assessment.
4. For recurrences from days 8–30, require a meaningful phase change or major update rather than ordinary continuation. Long-running stories remain in Persistent World State and dashboards until such a phase change occurs.
5. Continuation, unchanged policy, repeated statements, "talks continue", "markets await", post-release discussion, strategic significance "continuing to emerge", or a new example that merely restates an existing thesis have effectively zero Information Gain and cannot consume a Top Headlines slot.
6. Thesis-level deduplication is mandatory. For example, several different AI data-center investments cannot each be promoted merely to repeat "AI CapEx continues expanding"; the new case must materially change scale, geography, financing, demand evidence, economics, or another substantive belief.
7. Bayesian Update must explicitly answer internally: **What does today's evidence make us believe differently from the existing Persistent World State?** If the answer is "nothing material", reject the candidate from Top Headlines.
8. Prefer a somewhat less globally important but genuinely new event over a more important recurring story with insufficient Information Gain.
9. Persistent World State is the durable cross-edition memory. A story may remain there without re-entering Top Headlines. Dashboards may carry unchanged context and benchmark values, but must not present them as new developments.
10. The run log must record the deduplication audit: history window checked, material recurring candidates rejected, any recurring candidate admitted, and the concrete Information Gain that justified re-entry. This is internal-only and must never appear in published text/audio.
11. Editorial prose must not manufacture novelty by explaining why an old story is "still important." The gate is applied before ranking and drafting: **candidate → historical event/thesis match → Information-Gain pass/fail → ranking → writing**.

This gate supplements, and does not replace, the existing Global Significance Lens, Persistent World State, Bayesian Update / Information Gain, China source policy, written/spoken editorial rules, safety rules, source requirements, dashboards, or publication contract.

### Written-edition sensitive-term safety gate

The public written Daily Brief must satisfy this constraint **during generation first**, then pass deterministic validation before publication. This safety constraint must preserve as much substantive information as possible under the existing written-edition standards.

1. **Generation-time constraint is primary.** During research synthesis and drafting, proactively choose factual, neutral wording that does not contain politically sensitive blocked terms. Do not first write disallowed wording and plan to delete it later.
2. Preserve information density. When a relevant development is editorially important, prefer a semantically equivalent neutral institutional description, paraphrase, or higher-level factual formulation that retains the material facts, causal relevance, market implications, and reader value.
3. Do not omit an otherwise qualifying written-edition item merely because one obvious phrasing contains a blocked term if the same facts can be conveyed accurately with safe wording.
4. Do not distort facts, invent euphemistic claims, or add political interpretation merely to avoid terminology. If accurate safe wording cannot preserve the essential claim, downgrade or omit the item rather than publish blocked wording.
5. Before writing the canonical artifact to `_drafts/YYYY-MM-DD-daily-brief.md`, perform an internal full-text sensitive-term check and revise any matching sentence before commit.
6. After canonical handoff, validate the staged written artifact against the maintained sensitive-term list before Podcast-first release can complete and again before promotion to the public post.
7. If deterministic validation still detects a blocked term, keep the written edition staged/unpublished and revise the relevant sentence. Downstream deletion is last-resort fail-safe only, not the normal editorial mechanism.
8. The check applies to public article prose, headings, captions, summaries, and other reader-facing written content. Internal run logs and operational artifacts remain internal and are not reader-facing.
9. Never mention the blocked-term check, sensitive terms, platform review, filtering, censorship, or this safety gate in published written or spoken content.
10. **North Korea exclusion and foreign-leader guard.** Podcast platform review has rejected an episode that named the North Korean leader in a missile-test item. By owner decision, do not cover North Korea (DPRK) news at all in written or spoken editions, including headlines, dashboards, watch lists, and Persistent World State; do not name North Korean leadership (for example `金正恩`). Apply the same caution to naming foreign heads of state in military or security contexts when an institutional attribution conveys the same facts.

11. **Foreign elections in spoken editions: market-relevant and neutral only.** By owner decision, foreign election coverage (results, polls, campaigns, runoffs) always qualifies for the written edition under the normal gates, and may also enter the spoken/podcast derivative only when it has a clear, material market impact (for example on a major economy's equities, currency, sovereign bonds, commodities, or emerging-market risk). Spoken wording must stay neutral and factual, modeled on the 2026-10-05 Brazil paragraph that synthesized and passed platform review: state the vote shares, the gap, the runoff date, how the result compares with final polls, and the market reaction or what markets will price next. Avoid vote-counting procedure and electoral-authority detail, ideological labels (for example 右翼/左翼), candidate quotes, campaign narrative, and loaded adjectives. Keep it to one short paragraph. If the TTS service refuses an election paragraph (for example xfyun 26006 on that segment), remove the paragraph from the spoken script rather than delaying publication; the written edition keeps the story.
12. **Minimize strongly political topics in spoken editions.** By owner decision, the spoken/podcast derivative carries as little strongly political material as possible (foreign elections follow rule 11): domestic or party campaigns, party politics, leaders' political statements, coups and protests, wars and military operations, sanctions, diplomatic disputes, and similar political-security news. Include such a topic in spoken copy only when it has immediate, direct, and material market, energy, supply-chain, or technology impact, and then describe only that economic or market consequence briefly with neutral institutional attribution, without political narrative, quotes, or named political leaders where avoidable. The written edition keeps its normal editorial standards; the spoken script does not need to mirror every written headline and has no headline floor.

Operational priority: **safe generation → preserve information via neutral rephrasing → pre-handoff self-check → deterministic publication validation → last-resort blocking.**

### Reader-facing prose style

- In all reader-facing written Daily Brief and Weekly Review prose, avoid contrastive/corrective framing that creates a rhetorical foil before stating the point. Prohibited or strongly avoided forms include `不是……而是……`, `并不是……而是……`, `不是 X，是 Y`, `与其说 A，不如说 B`, `真正值得关注的不是 A，而是 B`, `关键不在 A，在 B`, and close variants.
- State the intended conclusion directly in affirmative, factual language. When a genuine comparison or distinction is necessary, describe the two facts explicitly without using the `不是……而是……` frame.
- This is a prose-style rule only; it must not alter factual meaning, uncertainty, nuance, source attribution, or information density.

### Editorial invisibility for internal selection logic

All research, selection, deduplication, ranking, Bayesian-update, Information-Gain, safety, source-policy, and workflow mechanics are internal editorial logic and must remain invisible in published written and spoken editions.

- Never publish explanations such as "this item was excluded as duplicate", "there was no sixth qualifying candidate", "we are not repeating yesterday's story", "this was retained only in Persistent World State", "this source was chosen because of source policy", or similar process commentary.
- Do not turn an empty Top Headlines slot into a meta-editorial item. Follow the applicable edition's headline-count contract: the Monday–Saturday Daily Brief has a hard minimum of six qualifying headlines, so continue research and keep the edition staged if that minimum is not met; never expose the shortfall or selection process in public copy. For other formats, follow their own editorial contract.
- Published prose should contain only the resulting factual/editorial product: the selected developments, evidence, implications, dashboards, and reader-facing analysis. It must not narrate how candidates were accepted, rejected, deduplicated, filtered, ranked, sourced, or safety-checked.
- Internal reasoning may be recorded only in the internal run log or other explicitly internal operational artifacts, never in canonical/public written copy, spoken scripts, RSS descriptions, show notes, or public pages.

### Early checkpoint and resumable-run contract

Every scheduled Daily Brief / Weekly Review run must behave as a resumable state machine.

1. Immediately after reading both authoritative SOPs and resolving the Asia/Shanghai date, before substantial research, create or idempotently update `ops/daily-brief-runs/YYYY-MM-DD.json` with status `started`, run type, start time, and known artifact state.
2. Update the same run log after each durable milestone: `started -> research_complete -> written_staged -> spoken_committed -> podcast_verified -> written_published -> published_verified`.
3. Before doing work, inspect the same-date run log plus canonical GitHub-main artifacts. If a partial run already exists, resume from the first incomplete durable milestone rather than restarting completed work.
4. GitHub-main artifacts and committed Podcast RSS are authoritative over stale run-log state. Reconcile the run log to verified durable state before resuming.
5. Preserve same-date idempotence and the versioned-enclosure rework contract. Recovery is not a new edition.
6. On failure, record `failure_stage` and concise internal `failure_detail` when GitHub access is still available. Do not delete valid upstream artifacts.
7. If Podcast is already verified, retry only written synchronization/deploy. If spoken canonical exists but Podcast is unverified, resume Podcast publication. If only the written draft exists, continue from spoken derivation. If no canonical artifacts exist, resume research/generation.
8. If the Daily Brief schedule is unexpectedly disabled, re-enable that existing schedule without changing cadence or prompt unless an intentional configuration change is separately requested; then use same-date checkpoint/artifact state to determine whether recovery is needed.
9. Checkpoint and recovery mechanics are internal only and must never appear in public written text, spoken audio, shownotes, RSS descriptions, or metadata.

Daily Brief / Weekly Review publishing order is mandatory:
1. Research and compose the canonical written edition and derive the canonical spoken edition under the current Daily/Weekly editorial contract.
2. Save the written edition to `_drafts/YYYY-MM-DD-daily-brief.md` and the spoken derivative to `handoffs/YYYY-MM-DD-spoken.txt` in this repository. Prefer one durable commit containing both same-date artifacts plus checkpoint/run-state changes when practical.
3. The handoff push triggers `Dispatch Podcast Handoff`, which dispatches the Podcast repository's `Ingest Daily Handoff`. The normal scheduled ChatGPT run does not directly create or update Podcast `episodes/` files.
4. `Ingest Daily Handoff` validates the handoff, creates the canonical same-date Podcast `episodes/epNNN-daily-YYYY-MM-DD.txt` when needed, and explicitly dispatches `Auto Publish Daily`. Do not rely on a GitHub-token-authored push recursively triggering another workflow.
5. The Podcast repository's `Auto Publish Daily` workflow generates TTS, publishes/replaces the final MP3 in R2, and upserts/verifies Podcast RSS.
6. This repository's `Publish Daily After Podcast` workflow starts from the staged draft, performs deterministic written sensitive-term validation, and waits for the matching dated Podcast item to appear in the committed Podcast `feed.xml` with a real enclosure URL, byte length, and duration.
7. Immediately before promotion, the written artifact is validated again. Only then does the workflow move the staged draft to `_posts/`, write the exact Podcast enclosure URL into `_data/audio.json`, build/deploy GitHub Pages itself, and verify that the live Daily Brief page contains the correct date title and exact final audio URL.

### Spoken opening convention

Every canonical Daily Brief spoken script must begin with the fixed spoken identifier and date:

`龙虾日报，YYYY年M月D日。`

- Keep this opening in every normal generation and every same-date rework.
- Use natural spoken Chinese month/day formatting without zero-padding (for example, `龙虾日报，2026年9月7日。`).
- This opening is reader-facing program identity, not internal editorial metadata, and must not be removed by deduplication, safety filtering, TTS normalization, or rework cleanup unless a separate explicit policy requires it.

### Same-date rework contract

A Daily Brief that is rejected, corrected, or materially regenerated after its first publication must use the same-date rework path end-to-end. Editing canonical text alone is not a completed rework.

1. Regenerate/update the same dated canonical written artifact and the same dated canonical spoken script; never create a duplicate date or episode.
2. Commit the corrected written artifact and corrected spoken handoff to their canonical staging locations in `daily_brief`, then let the GitHub-native handoff ingestion update the Podcast canonical episode. Perform GitHub-main read-back verification before downstream publication.
3. The spoken-script update must run the Podcast same-date publish path, including spoken safety validation, TTS normalization, TTS regeneration, R2 replacement/versioning, Podcast RSS upsert, and verification of the final enclosure URL, byte length, and duration.
4. After Podcast RSS reflects the replacement audio, the written repository must re-read the committed Podcast `feed.xml` for that date and update `_data/audio.json` to the **exact current enclosure URL**. Never assume that a same-date retry keeps the previous MP3 URL; versioned objects such as `-v2`, `-v3`, etc. are expected.
5. Updating the spoken script or Podcast RSS is not sufficient. The written page must be redeployed after the audio mapping changes.
6. Final rework verification is end-to-end and mandatory: Podcast RSS date/guid → final enclosure URL/length/duration → `daily_brief/_data/audio.json` exact URL equality → deployed written page contains that exact enclosure URL and the corrected written content. A mismatch at any point means the rework is incomplete.
7. Same-date retries remain idempotent: update the existing dated written post, existing spoken script, existing Podcast item/guid, existing audio mapping key, and existing run-log file. Do not append duplicate episodes or duplicate dated artifacts.
8. The internal run log at `ops/daily-brief-runs/YYYY-MM-DD.json` must record rework reason, canonical commit SHAs, Podcast replacement result, final RSS enclosure URL/length/duration, audio-mapping refresh, written redeploy result, and final end-to-end verification status.
9. Failure handling preserves repository boundaries: if TTS/R2/RSS replacement fails, do not point the written page at an unverified audio object; if Podcast replacement succeeds but written mapping/deploy fails, preserve the valid Podcast item and retry only the written synchronization/deploy stage.
10. A rework is complete only when the corrected written edition and corrected spoken audio are both the versions reachable from the public written Daily Brief page. Canonical handoff alone must never be reported as a completed rework.

The two repositories do not require a cross-repository write token. They synchronize through the committed Podcast RSS. If Podcast publication fails, the dated written Brief remains staged and unpublished. If Podcast succeeds but the written workflow fails, keep the Podcast episode and rerun `Publish Daily After Podcast` for that date. Re-runs must remain idempotent.

`future: true` remains enabled in `_config.yml` so a same-day staged post can be published safely even when its canonical front-matter timestamp is later than the actual scheduler time; `_drafts/` remains unpublished unless explicitly moved to `_posts/`.

## Sunday Weekly Review editorial contract

The Sunday edition is a **Weekly Review**, not a normal 24-hour Top-Headlines digest.

- Review the full prior week and focus on what materially changed the Persistent World State: which beliefs were strengthened, weakened, reversed, or newly established; the week's highest-information developments; important market, AI, semiconductor, world, and China developments under the existing editorial rules; and what matters most for the coming week.
- Do not merely concatenate or summarize the previous seven Daily Briefs. Apply the same event-level and thesis-level semantic deduplication and Information-Gain discipline to avoid repetitive retelling.
- The public written title remains the date only in `YYYY-MM-DD` format; do not prefix it with `Weekly Review` or `Daily Brief`.
- The Sunday spoken script follows the common spoken conventions and Podcast-first release contract, including the fixed `龙虾日报，YYYY年M月D日。` opening. Its first reader-facing sentence after that opening is fixed as `周日这期，我们总结本周的状态。`
- The former standalone **AI 信用周期** research is integrated as a dedicated section in both the canonical written Weekly Review and its spoken/podcast derivative. Analyze developments since the previous Sunday review, not merely Sunday news.
- Nvidia is a major but non-exclusive node. Also cover OpenAI, Anthropic, hyperscalers, neoclouds, data centers, power, project finance/private credit, bond markets, and final enterprise/consumer demand when there is material evidence.
- Monitor, where material: financing and supplier guarantees/residual-value/lease/buyback support; OpenAI/Anthropic/neocloud financing and long-term compute obligations; GPU rental prices/utilization/secondary residual values; project-finance costs and credit spreads; consumer paid users/ARPU/retention/token and inference volumes; Claude Code/Codex and other coding-agent paid usage/workloads; enterprise contracts/API consumption/renewals/pilot-to-production; OpenAI/Anthropic revenue/ARR, gross margin, inference costs, cash burn and FCF; AWS/Azure/GCP AI revenue, GPU utilization and inference mix; and measurable labor substitution, actual cost reduction, incremental revenue and productivity gains.
- Strictly distinguish genuine outside-AI cash demand from VC funding, cloud credits, vendor financing, circular investment or subsidies. Compare AI revenue/economic value with hyperscaler/AI-company CapEx, depreciation, power and financing costs, and assess whether the AI revenue / AI infrastructure investment gap is narrowing or widening.
- Maintain the AI Hard Cash ROI evidence framework. Give highest weight to actual incremental revenue, Opex/labor-cost reductions, headcount avoidance, gross-margin/operating-profit/FCF improvement, and prefer filings, annual reports, earnings calls, regulatory disclosures and other primary evidence over vendor-sponsored surveys or hours-saved estimates.
- If there is no meaningful weekly change, keep the AI Credit Cycle section very short rather than manufacturing content.
- Do not create or update standalone `_posts/YYYY-MM-DD-ai-credit-cycle.md` posts or `ai-credit-cycle.xml`; they remain historical archive only.

## 2. AI 信用周期 — historical standalone archive

The former standalone AI 信用周期 stream is now historical-only.

- Existing canonical posts remain at `_posts/YYYY-MM-DD-ai-credit-cycle.md`.
- Existing layout/permalinks and `ai-credit-cycle.xml` remain available as a historical archive.
- No active schedule creates or updates standalone AI 信用周期 posts or its RSS.
- New AI 信用周期 research is integrated into the Sunday Weekly Review canonical written edition and its spoken/podcast derivative.
- The integrated Sunday section preserves the same scope: Nvidia as a major but non-exclusive node, OpenAI/Anthropic, hyperscalers, neoclouds, data-center/project finance, private credit, GPU leasing/residual values, real outside-AI demand, AI CapEx economics, and hard-cash enterprise ROI.
- The Sunday section must distinguish outside-AI cash flow from VC/cloud-credit/vendor-financing/circular demand and maintain the Hard Cash ROI evidence framework.
- If there is no material weekly change, keep the section brief rather than manufacturing content.

## Daily AI Credit Cycle Pulse

The normal Monday–Saturday Daily Brief includes a dedicated **AI Credit Cycle Pulse / AI 信用周期脉冲** section in the canonical written edition.

- The section monitors only fresh incremental evidence relevant to the AI credit cycle: frontier-model company financing and cash burn; hyperscaler/neocloud CapEx and long-term compute obligations; GPU/server leasing, utilization and residual values; data-center/project finance, private credit and bond-market conditions; supplier financing/guarantees/buybacks; power and infrastructure funding; enterprise/consumer paid demand; AI revenue/ARR, gross margin, inference costs and FCF; and measurable hard-cash ROI such as incremental revenue, Opex/labor-cost reduction, headcount avoidance, margin or cash-flow improvement.
- Distinguish genuine outside-AI cash demand from VC funding, cloud credits, vendor financing, circular capital flows, subsidies, or accounting-only demand.
- Apply the same rolling event/thesis semantic deduplication and Information-Gain gate as the rest of Daily Brief. Do not restate “AI CapEx remains strong” or similar standing theses without new evidence that changes scale, financing, demand quality, economics, or risk.
- The written section is structurally present each normal Daily Brief but may be very short when there is little new evidence. A concise “no material change in cycle assessment” is acceptable internally as a state update, but published wording must remain reader-facing and must not expose dedup/editorial mechanics.
- The spoken derivative includes this section only when there is material new information worth the listener’s time; otherwise it may be omitted from the spoken script.
- Sunday Weekly Review remains the full weekly synthesis of the AI credit cycle and should integrate the week's Daily Pulse evidence into a higher-level cycle assessment rather than replay each daily item.
- The historical standalone AI 信用周期 archive remains unchanged and is not reactivated as a separate daily publication stream.

## Number of the Day, Compute & Supply-Chain Dashboard, and Call Review

Three standing sections added by owner decision on 2026-10-07. They apply to the Monday–Saturday Daily Brief; Sunday handling is noted below. All of them follow the existing source, Information-Gain, deduplication, safety, and editorial-invisibility rules.

Written section order: opening summary paragraph → **Number of the Day / 今日数字** → Top Headlines → AI Credit Cycle Pulse → **Compute & Supply-Chain Dashboard / 算力与供应链看板** → Markets Dashboard → China Dashboard → AI × Employment Watch → Science Watch → Persistent World State / Bayesian Update → **Call Review / 判断复盘** → What to Watch Today.

### Number of the Day / 今日数字

- One sourced number that best captures the edition's main thread, with one or two sentences on why it matters, for example `5.31%：美国十年期国债收益率，为 2007 年以来最高`.
- Prefer a number from the day's Top Headlines or dashboards, with a clear unit, date, and source link. Do not invent derived figures; a simple stated calculation from sourced inputs is acceptable when labeled as an estimate.
- Avoid numbers whose main meaning is political (election shares, casualty counts, sanctions totals); choose an economic, market, technology, or science number instead.
- Spoken: include it as one short paragraph right after the opening summary paragraph.

### Compute & Supply-Chain Dashboard / 算力与供应链看板

- A fixed set of hard indicators for AI compute economics. Report only indicators with a new data point since the previous edition; if none moved, a single line stating that no tracked indicator changed is enough.
- Tracked indicators (add others only when durable and regularly published): GPU rental and long-term lease prices (per GPU-hour, by chip class); HBM, DRAM, and NAND contract or spot prices; TSMC monthly revenue and other foundry/packaging capacity signals (for example CoWoS); hyperscaler and neocloud CapEx guidance and actuals; data-center power prices, interconnection, and capacity additions; accelerator shipment or lead-time data.
- Each entry gives the new value, the previous comparable value with its date, and the source. Keep an internal ledger of last-known values at `ops/compute-dashboard.json` (indicator, value, unit, as-of date, source URL) and update it in the same commit as the staged draft; use it for comparisons instead of re-deriving history.
- Distinguish list prices, reported deal terms, and estimates. Deal-derived figures (for example the 2026-10-05 Tencent–Oracle lease at roughly USD 1.6 per chip-hour) must be labeled as estimates from reported terms.
- Spoken: mention only when a tracked indicator moved materially; otherwise omit.

### Call Review / 判断复盘

- Revisit one or two specific earlier judgments from prior editions' Persistent World State, Bayesian Update, or analysis when new evidence now tests them. Cite the edition date of the original call, quote or closely paraphrase it, present the new evidence with sources, and grade it as `成立`, `部分成立`, `不成立`, or `仍待验证`.
- Grade honestly, including misses; never reword the original call after the fact to make it look right. Do not manufacture reviews: if no earlier call was materially tested by new evidence, omit the section from the written edition rather than padding it.
- Prefer calls about markets, rates, energy, AI economics, technology, and China business; avoid political forecasts.
- Record internally in the run log which calls were reviewed and their grades.
- Spoken: include only a call graded `成立` or `不成立` on clear evidence, in two or three sentences; otherwise omit.

### Sunday Weekly Review

- Number of the Day becomes **本周数字** (one number for the week).
- Call Review becomes a fuller weekly section covering the week's tested calls, graded the same way.
- The Compute & Supply-Chain Dashboard is folded into the Weekly Review's AI 信用周期 section as a week-over-week indicator summary.

## AI and employment impact watch

AI's impact on employment is a persistent Daily Brief research theme, covering both positive and negative effects. It does not receive a mandatory daily headline slot; items enter the edition only when they clear the existing Global Significance Lens, rolling semantic-deduplication, Bayesian Update, and Information-Gain gates.

- Track direct evidence of AI-related layoffs, hiring reductions or freezes, lower demand for entry-level roles, role elimination or task substitution, changes in hours, wages, contractor demand, and occupational composition.
- Track positive employment effects as well: new AI-related roles and occupations, AI-driven business expansion and hiring, productivity-linked growth, AI-skill wage premiums, worker augmentation, and evidence that automation reallocates workers rather than eliminating employment.
- Prefer observed labor-market outcomes and measurable company behavior over forecasts or executive claims about hypothetical future job losses or gains. Useful evidence includes official labor statistics, payroll/job-posting data, company headcount and hiring disclosures, wage data, longitudinal studies, and credible large-sample research.
- Distinguish AI causality from ordinary restructuring, macroeconomic weakness, offshoring, post-pandemic normalization, mergers, or unrelated cost cutting. When causality is uncertain, state that uncertainty rather than attributing the employment change to AI.
- Evaluate both aggregate and distributional effects: total employment may differ from effects on particular occupations, junior versus senior workers, skill groups, industries, regions, wages, hours, and career-entry pathways.
- Track realized productivity effects as a bridge between AI adoption, enterprise ROI, and labor demand: output per worker, time saved, throughput, margins, staffing ratios, and whether productivity gains lead to expansion/hiring or primarily headcount avoidance/reduction.
- Track distribution of AI's economic gains: wage changes, AI-skill wage premiums, labor share versus capital returns, and whether gains accrue broadly to workers or are concentrated among particular skills, firms, or capital owners.
- Do not force this theme into every edition. Persistent trends belong in Persistent World State; publish a headline or analysis only when new evidence materially changes the current assessment.
- When material, incorporate the evidence into the normal AI/economy coverage and Sunday Weekly Review rather than creating a separate publication stream.

## Watchdog recovery execution contract

Both Watchdogs are recovery workers, not observers, and use the durable-state recovery model defined above.

- **Paired-schedule lifecycle check:** at the start of recovery, inspect the paired main recurring automation (`Daily Brief` for Mon–Sat, `Weekly Review` for Sunday). If it is unexpectedly disabled, re-enable that exact task without changing its prompt, cadence, timezone, or other configuration. Never disable the paired main task or the Watchdog itself as part of a content run.
- **Concurrency guard:** do not race a healthy main run. Treat the main run as active and exit without publication side effects when a relevant GitHub Actions run is queued/in_progress or same-date durable artifacts/checkpoints have progressed within roughly the previous 15 minutes. Take over only when state is missing, stale, failed, or durable evidence proves recovery is required.
- If no same-date run log or canonical artifacts exist because the main schedule failed before checkpointing, execute the normal same-date Daily Brief or Weekly Review flow under the current SOPs.
- If partial durable state exists, resume from the first incomplete milestone rather than repeating completed upstream work.
- If durable public state is already equivalent to `published_verified`, exit without publication side effects; reconcile a stale run log only when needed.
- Downstream recovery must use one authoritative side-effect path at a time. Never hand-edit public post/audio mapping while a canonical publish workflow recovery is active.
- When deciding whether to rerun a failed `Publish Daily After Podcast` run, compare its `head_sha` with current `main`. Rerun only when they match and rerun is the safe idempotent path. If `main` has advanced, the failed run is stale: dispatch the canonical workflow from current `main` for the exact date instead.
- After recovery, independently verify the durable/public contract: dated public post exists, `_data/audio.json` exactly matches the committed Podcast RSS enclosure for that date, and the live page contains the correct date/title and exact final audio URL. Workflow success alone is insufficient.
- If recovery still fails, preserve valid upstream artifacts, record `failure_stage` and concise `failure_detail` when possible, and leave all recurring automations enabled.

## Isolated release test environment

Production workflow changes should be validated through isolated test paths before relying on them in scheduled production runs.

- `Test Daily Release Harness` (`.github/workflows/test-daily-release-harness.yml`) is the deterministic written-publication/recovery harness.
- It accepts only synthetic dates in the 2050–2099 range, uses temporary fixture directories, and runs with read-only repository permissions.
- It must never receive production R2 credentials, write the production Podcast feed, push publication state to `main`, deploy production Pages, or send production notifications.
- The harness reuses the real deterministic publication scripts against fixtures rather than maintaining a second implementation of publication logic.
- Required scenarios include: happy path, missing Podcast item, duplicate same-date Podcast GUID lineage, audio mapping mismatch, and already-published/idempotent replay. Additional recovery/state-machine regressions should be added here as they are discovered.
- `scripts/check_release_state.py` is a non-mutating machine-readable state checker. In tests it reads fixture root/feed/optional saved HTML only and never fetches or writes production resources.
- Podcast/TTS behavior is tested separately by the Podcast repository's isolated Mock workflows. These layers together form the supported pre-production test environment.
- A passing test harness does not itself authorize production publication; production still follows the normal SOP, durable-state, and end-to-end verification contracts.

## Schedule architecture

- Monday–Saturday: normal **Daily Brief at 07:00 Asia/Shanghai**, optimized for breakfast/commute listening before the main China/Hong Kong cash-equity open. Monday is no longer a separate schedule; it uses the same Daily Brief task and the same research/publishing contract as Tuesday–Saturday, while still applying rolling deduplication against the Sunday Weekly Review and prior history.
- Do **not** routinely repeat a boilerplate sentence stating that China mainland/Hong Kong cash-equity markets have not yet entered normal trading (for example, `北京时间 07:00 前，中国内地和香港主要现金股票市场尚未进入正常交易时段。`). Omit this by default from both written and spoken editions. Mention pre-open/open status only when it is materially necessary to interpret a specific market move, distinguish overnight/indicative data from the current cash session, or prevent a concrete factual ambiguity.
- Monday–Saturday recovery: **Daily Brief Watchdog at 07:30 Asia/Shanghai**. It is an actionable recovery worker, not an observer: if the same-date run is already `published_verified`, it exits without side effects; otherwise it resumes idempotently from the first incomplete durable milestone, actively reruns/dispatches the canonical GitHub Actions recovery path when a downstream stage has failed, waits for that recovery path, and verifies durable/public artifacts before considering recovery complete. Before rerunning a failed Actions run, compare its `head_sha` with current `main`: rerun only when they still match. If `main` has advanced, treat the run as stale and dispatch the canonical workflow from current `main` for the exact date instead; do not rerun an old checkout that can rebase-conflict with newer `_data/audio.json` or publication state. It may re-enable the existing Daily Brief schedule if unexpectedly disabled. It never touches Sunday Weekly Review.
- Monday–Saturday GitHub reconciliation: **Reconcile Daily Publication at 08:00 Asia/Shanghai**. This is a narrow second recovery layer for the Podcast-first downstream boundary. If the same-date staged draft still exists and the committed Podcast RSS item validates, it dispatches the existing `Publish Daily After Podcast` workflow for that exact date. If the post is already public, the draft is absent, or Podcast is not yet verified, it exits without publication side effects.
- Sunday: the combined **Daily Brief Work** scheduled task runs at **07:00 Asia/Shanghai** and selects the Weekly Review edition, including the integrated AI 信用周期 section in both written and spoken/podcast editions. There is no separate Weekly Review scheduled task.
- Recovery Watchdogs remain separate recovery-only tasks and are currently paused; the combined Daily Brief Work run does not invoke either Watchdog.
- Sunday GitHub reconciliation: **Reconcile Daily Publication at 10:00 Asia/Shanghai** applies the same narrow Podcast-verified/still-staged downstream recovery rule to the Sunday edition.
The combined Daily Brief Work schedule, any separately re-enabled Watchdog, and GitHub reconciliation all respect the same repository boundaries and durable-state/idempotence contracts. Recovery must use one authoritative side-effect path at a time and must never create a separate content edition.

## Repository boundary

`tangkk/daily_brief` remains a written-site repository. Podcast-specific assets and workflows belong only in `tangkk/lobster-daily-podcast`.


## GitHub-native spoken handoff contract

Normal Daily Brief / Weekly Review production must minimize ChatGPT connector writes and must not require a direct ChatGPT write to the Podcast repository.

1. The scheduled ChatGPT run owns research, the canonical written draft, the canonical spoken derivative, and initial durable state in `tangkk/daily_brief`.
2. The canonical spoken derivative is staged in this repository at `handoffs/YYYY-MM-DD-spoken.txt`. It must already satisfy the Podcast SOP's spoken opening, editorial, safety, language, prose-style, and pronunciation rules before handoff.
3. The preferred durable handoff is a single `daily_brief` commit containing the same-date written draft, spoken handoff, and checkpoint/run-state changes when practical. Do not perform a second ChatGPT connector write to `tangkk/lobster-daily-podcast` during the normal daily release path.
4. A push changing `handoffs/*-spoken.txt` triggers `Dispatch Podcast Handoff`, which dispatches the Podcast repository's `Ingest Daily Handoff` workflow. Cross-repository dispatch uses the repository secret `PODCAST_DISPATCH_TOKEN`; keep its permissions minimal and scoped to the Podcast repository.
5. The Podcast repository ingests the exact handoff, allocates/reuses the canonical same-date episode path idempotently, commits it with GitHub Actions, and explicitly dispatches the existing `Auto Publish Daily` TTS/R2/RSS chain. Do not rely on a `GITHUB_TOKEN`-authored push to recursively trigger another workflow.
6. GitHub-native scheduled reconciliation in the Podcast repository independently checks for a same-date handoff. This is the recovery path if the event-driven cross-repository dispatch is missed or temporarily unavailable.
7. After Podcast verification, the existing written publication/reconciliation path remains authoritative for promotion to `_posts/`, exact audio mapping, Pages deployment, and live verification.
8. The ChatGPT Daily Brief Watchdog is the final recovery layer. It should inspect durable state and GitHub-native workflow outcomes first; it must not default to recreating the old direct ChatGPT-to-Podcast spoken commit path.
9. Direct ChatGPT writes to `tangkk/lobster-daily-podcast` remain valid for explicit Podcast maintenance, workflow/SOP/TTS/pronunciation changes, or an explicitly requested exceptional repair. They are not part of normal Daily Brief publication.
10. Same-date idempotence and rework rules remain unchanged. A differing already-ingested same-date spoken script must fail closed and use the explicit same-date rework contract rather than silently overwrite canonical Podcast source.

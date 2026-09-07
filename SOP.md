# Daily Brief SOP

The site contains two written content streams with different publishing rules.

## 1. Daily Brief written edition — `tangkk/daily_brief`

- Staged canonical posts: `_drafts/YYYY-MM-DD-daily-brief.md`
- Public canonical posts: `_posts/YYYY-MM-DD-daily-brief.md`
- Layout: `daily_brief`
- Public site: https://tangkk.github.io/daily_brief/
- Written RSS: https://tangkk.github.io/daily_brief/feed.xml
- The written site may play the already-published podcast MP3 only from an explicit `_data/audio.json` mapping.
- It never generates TTS, uploads audio, owns podcast metadata, or guesses an R2 URL.

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

### Editorial invisibility for internal selection logic

All research, selection, deduplication, ranking, Bayesian-update, Information-Gain, safety, source-policy, and workflow mechanics are internal editorial logic and must remain invisible in published written and spoken editions.

- Never publish explanations such as "this item was excluded as duplicate", "there was no sixth qualifying candidate", "we are not repeating yesterday's story", "this was retained only in Persistent World State", "this source was chosen because of source policy", or similar process commentary.
- Do not turn an empty Top Headlines slot into a meta-editorial item. If fewer than the target number of genuinely qualifying headlines exist, simply publish fewer headlines, unless another existing content rule explicitly requires a fixed count; in that case continue research for a qualifying item rather than exposing the selection process.
- Published prose should contain only the resulting factual/editorial product: the selected developments, evidence, implications, dashboards, and reader-facing analysis. It must not narrate how candidates were accepted, rejected, deduplicated, filtered, ranked, sourced, or safety-checked.
- Internal reasoning may be recorded only in the internal run log or other explicitly internal operational artifacts, never in canonical/public written copy, spoken scripts, RSS descriptions, show notes, or public pages.


Daily Brief publishing order is mandatory:
1. Research and compose the canonical written Daily Brief.
2. Save that exact edition to `_drafts/YYYY-MM-DD-daily-brief.md`. This is the release staging input, not the public post path.
3. Create and commit the spoken derivative to `tangkk/lobster-daily-podcast/episodes/`.
4. The Podcast repository's `Auto Publish Daily` workflow generates TTS, publishes/replaces the final MP3 in R2, and upserts/verifies Podcast RSS.
5. This repository's `Publish Daily After Podcast` workflow starts from the staged draft and waits for the matching dated Podcast item to appear in the committed Podcast `feed.xml` with a real enclosure URL, byte length, and duration.
6. Only then does it move the staged draft to `_posts/`, write the exact Podcast enclosure URL into `_data/audio.json`, build/deploy GitHub Pages itself, and verify that the live Daily Brief page contains both the correct Daily Brief title and exact final audio URL.

### Same-date rework contract

A Daily Brief that is rejected, corrected, or materially regenerated after its first publication must use the same-date rework path end-to-end. Editing canonical text alone is not a completed rework.

1. Regenerate/update the same dated canonical written artifact and the same dated canonical spoken script; never create a duplicate date or episode.
2. Commit both canonical artifacts to their owning repositories and perform GitHub-main read-back verification before downstream publication.
3. The spoken-script update must run the Podcast same-date publish path, including spoken safety validation, TTS normalization, TTS regeneration, R2 replacement/versioning, Podcast RSS upsert, and verification of the final enclosure URL, byte length, and duration.
4. After Podcast RSS reflects the replacement audio, the written repository must re-read the committed Podcast `feed.xml` for that date and update `_data/audio.json` to the **exact current enclosure URL**. Never assume that a same-date retry keeps the previous MP3 URL; versioned objects such as `-v2`, `-v3`, etc. are expected.
5. Updating the spoken script or Podcast RSS is not sufficient. The written page must be redeployed after the audio mapping changes.
6. Final rework verification is end-to-end and mandatory: Podcast RSS date/guid → final enclosure URL/length/duration → `daily_brief/_data/audio.json` exact URL equality → deployed written page contains that exact enclosure URL and the corrected written content. A mismatch at any point means the rework is incomplete.
7. Same-date retries remain idempotent: update the existing dated written post, existing spoken script, existing Podcast item/guid, existing audio mapping key, and existing run-log file. Do not append duplicate episodes or duplicate dated artifacts.
8. The internal run log at `ops/daily-brief-runs/YYYY-MM-DD.json` must record rework reason, canonical commit SHAs, Podcast replacement result, final RSS enclosure URL/length/duration, audio-mapping refresh, written redeploy result, and final end-to-end verification status.
9. Failure handling preserves repository boundaries: if TTS/R2/RSS replacement fails, do not point the written page at an unverified audio object; if Podcast replacement succeeds but written mapping/deploy fails, preserve the valid Podcast item and retry only the written synchronization/deploy stage.
10. A rework is complete only when the corrected written edition and corrected spoken audio are both the versions reachable from the public written Daily Brief page. Canonical handoff alone must never be reported as a completed rework.

The two repositories do not require a cross-repository write token. They synchronize through the committed Podcast RSS. If Podcast publication fails, the dated written Brief remains staged and unpublished. If Podcast succeeds but the written workflow fails, keep the Podcast episode and rerun `Publish Daily After Podcast` for that date. Re-runs must remain idempotent.

`future: true` is intentionally enabled in `_config.yml` so a same-day Daily Brief whose canonical front matter still says `08:00:00 +0800` can be deployed immediately after an earlier scheduled run; `_drafts/` remains unpublished unless explicitly moved to `_posts/`.

## 2. AI 信用周期 — written-only stream

AI 信用周期 is an independent written-only research stream hosted in this same repository.

- Canonical posts: `_posts/YYYY-MM-DD-ai-credit-cycle.md`
- Layout: `ai_credit_cycle`
- Canonical permalink: `/ai-credit-cycle/YYYY/MM/DD/`; it must never share the Daily Brief `/:year/:month/:day/` URL.
- No spoken script, TTS, MP3, R2 upload, Podcast RSS item, or audio player.
- It does not depend on Daily Brief Podcast publication and may be published independently.
- Research runs daily, but publish a dated article only when there is a meaningful new development, important case, risk signal, or structural change. Do not manufacture a post merely to fill every date.
- If no AI 信用周期 article exists for a date, the home page shows only Daily Brief for that date.
- If one exists, the home page shows `Daily Brief · AI 信用周期` beside the same date.
- The existing Daily Brief RSS remains Daily-Brief-only and excludes AI 信用周期 posts.

The AI 信用周期 scope covers Nvidia as a major but non-exclusive node, together with OpenAI, Anthropic, hyperscalers, neoclouds, data-center/project finance, private credit, GPU leasing/residual values, real end demand, AI CapEx economics, and hard-cash enterprise ROI.

## Repository boundary

`tangkk/daily_brief` remains a written-site repository. Podcast-specific assets and workflows belong only in `tangkk/lobster-daily-podcast`.

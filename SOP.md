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

### Previous-edition-first semantic deduplication

Before selecting Top Headlines for a new Daily Brief, read the previous day's canonical written edition first and treat it as the primary semantic-deduplication baseline.

- Any event/story already present in the previous edition is default-exclude from the new Top Headlines, even if it appears under a new headline, outlet, URL, or wording.
- A repeated story may re-enter Top Headlines only when there is material new information that changes the reader's state of knowledge or the editorial Bayesian assessment. Qualifying updates include a new quantitative fact, a new binding decision, implementation or enforcement, a material market reaction, a verified change in real-world conditions, or evidence that meaningfully changes prior expectations.
- Non-updates such as continuation, unchanged policy, repeated statements, "talks continue", "markets await", or commentary that merely rephrases an existing thesis have effectively zero Information Gain and must remain in Persistent World State / dashboards rather than consume a Top Headlines slot.
- Semantic identity is determined at the underlying event/thesis level, not by title, URL, publisher, entity ordering, or surface wording.
- Bayesian Update must answer: "What does today's evidence make us believe differently from yesterday?" If the answer is "nothing material", the story stays out of Top Headlines.
- Prefer a somewhat less globally important but genuinely new event over a more important story that is merely repeated from the prior edition.
- Persistent World State may continue carrying the background state of an ongoing story without causing it to re-enter Top Headlines.

Daily Brief publishing order is mandatory:
1. Research and compose the canonical written Daily Brief.
2. Save that exact edition to `_drafts/YYYY-MM-DD-daily-brief.md`. This is the release staging input, not the public post path.
3. Create and commit the spoken derivative to `tangkk/lobster-daily-podcast/episodes/`.
4. The Podcast repository's `Auto Publish Daily` workflow generates TTS, publishes/replaces the final MP3 in R2, and upserts/verifies Podcast RSS.
5. This repository's `Publish Daily After Podcast` workflow starts from the staged draft and waits for the matching dated Podcast item to appear in the committed Podcast `feed.xml` with a real enclosure URL, byte length, and duration.
6. Only then does it move the staged draft to `_posts/`, write the exact Podcast enclosure URL into `_data/audio.json`, build/deploy GitHub Pages itself, and verify that the live Daily Brief page contains both the correct Daily Brief title and exact final audio URL.

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

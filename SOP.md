# Daily Brief SOP

The site contains two written content streams with different publishing rules.

## 1. Daily Brief written edition — `tangkk/daily_brief`

- Canonical posts: `_posts/YYYY-MM-DD-daily-brief.md`
- Layout: `daily_brief`
- Public site: https://tangkk.github.io/daily_brief/
- Written RSS: https://tangkk.github.io/daily_brief/feed.xml
- The written site may play the already-published podcast MP3 only from an explicit `_data/audio.json` mapping.
- It never generates TTS, uploads audio, owns podcast metadata, or guesses an R2 URL.

Daily Brief publishing order is mandatory:
1. Research and compose the canonical written Daily Brief.
2. Create the spoken derivative in `tangkk/lobster-daily-podcast`.
3. Generate TTS and publish the final MP3 to R2.
4. Update and verify the Podcast RSS with the real enclosure URL, byte length, and duration.
5. Only after Podcast publication succeeds, publish the same canonical written Brief here and update `_data/audio.json` to the exact final enclosure URL.
6. Verify GitHub Pages and the written player.

If Podcast publication fails, do not publish that day's Daily Brief written post. Re-runs must be idempotent.

## 2. AI 信用周期 — written-only stream

AI 信用周期 is an independent written-only research stream hosted in this same repository.

- Canonical posts: `_posts/YYYY-MM-DD-ai-credit-cycle.md`
- Layout: `ai_credit_cycle`
- No spoken script, TTS, MP3, R2 upload, Podcast RSS item, or audio player.
- It does not depend on Daily Brief Podcast publication and may be published independently.
- Research runs daily, but publish a dated article only when there is a meaningful new development, important case, risk signal, or structural change. Do not manufacture a post merely to fill every date.
- If no AI 信用周期 article exists for a date, the home page shows only Daily Brief for that date.
- If one exists, the home page shows `Daily Brief · AI 信用周期` beside the same date.
- The existing Daily Brief RSS remains Daily-Brief-only and excludes AI 信用周期 posts.

The AI 信用周期 scope covers Nvidia as a major but non-exclusive node, together with OpenAI, Anthropic, hyperscalers, neoclouds, data-center/project finance, private credit, GPU leasing/residual values, real end demand, AI CapEx economics, and hard-cash enterprise ROI.

## Repository boundary

`tangkk/daily_brief` remains a written-site repository. Podcast-specific assets and workflows belong only in `tangkk/lobster-daily-podcast`.

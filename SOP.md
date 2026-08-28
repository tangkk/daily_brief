# Daily Brief SOP

Daily Brief is split into two independent publishing layers.

## 1. Written edition — `tangkk/daily_brief`

This repository owns the canonical written Daily Brief, written RSS/site, and a lightweight playback link to the already-published podcast audio in R2.

- Canonical posts: `_posts/YYYY-MM-DD-daily-brief.md`
- Public site: https://tangkk.github.io/daily_brief/
- Written RSS: https://tangkk.github.io/daily_brief/feed.xml
- Written pages may contain an HTML audio player, but they do not generate, upload, replace, or own audio.
- Historical R2 URLs may be kept in `_data/audio.json` only as written-site playback references; dates from 2026-08-21 onward use the shared deterministic R2 path when no explicit historical mapping is needed.
- No spoken scripts, TTS generation, podcast RSS, podcast artwork, R2 upload code, audio replacement logic, or podcast workflows belong in this repository.

The user-visible Daily Brief and the GitHub post must contain the same substantive prose. Only citation/rendering syntax may differ.

## 2. Podcast edition — `tangkk/lobster-daily-podcast`

All podcast-specific assets, audio ownership, metadata and workflow live in the dedicated podcast repository.

- Podcast RSS: https://tangkk.github.io/lobster-daily-podcast/feed.xml
- Podcast cover: `cover.jpg`
- Spoken canonical scripts: `episodes/*.txt`
- TTS preview / publish / audio replacement / notification workflows live there.
- The podcast audio in R2 is the single audio source of truth; the written site points to that same R2 object rather than creating a second copy.

The spoken script is a derivative of the written Daily Brief and may condense, reorder, and simplify for listening while preserving the day's important facts and analytical conclusions.

## Publishing order

1. Research and produce the canonical written Daily Brief.
2. Publish the exact substantive written version to `tangkk/daily_brief`.
3. Create the spoken derivative.
4. Put all spoken/podcast artifacts and audio operations in `tangkk/lobster-daily-podcast` only.
5. Once the podcast audio exists in R2, the written page plays that exact same R2 file; never upload a duplicate audio copy for the written site.

Keep the publishing layers separate while sharing the final R2 audio object for playback.

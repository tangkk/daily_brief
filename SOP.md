# Daily Brief SOP

Daily Brief is split into two independent publishing layers.

## 1. Written edition — `tangkk/daily_brief`

This repository contains only the canonical written Daily Brief and its written RSS/site.

- Canonical posts: `_posts/YYYY-MM-DD-daily-brief.md`
- Public site: https://tangkk.github.io/daily_brief/
- Written RSS: https://tangkk.github.io/daily_brief/feed.xml
- No spoken scripts, TTS, audio metadata, podcast RSS, podcast artwork, R2 upload code, or podcast workflows belong in this repository.

The user-visible Daily Brief and the GitHub post must contain the same substantive prose. Only citation/rendering syntax may differ.

## 2. Podcast edition — `tangkk/lobster-daily-podcast`

All podcast-specific assets and workflow live in the dedicated podcast repository.

- Podcast RSS: https://tangkk.github.io/lobster-daily-podcast/feed.xml
- Podcast cover: `cover.jpg`
- Spoken canonical scripts: `episodes/*.txt`
- TTS preview / publish / audio replacement / notification workflows live there.

The spoken script is a derivative of the written Daily Brief and may condense, reorder, and simplify for listening while preserving the day's important facts and analytical conclusions.

## Publishing order

1. Research and produce the canonical written Daily Brief.
2. Publish the exact substantive written version to `tangkk/daily_brief`.
3. Create the spoken derivative.
4. Put all spoken/podcast artifacts and operations in `tangkk/lobster-daily-podcast` only.

Never reintroduce podcast-specific files into `tangkk/daily_brief`.

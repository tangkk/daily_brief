# Daily Brief run logs

Each scheduled Daily Brief run should maintain one idempotent JSON record at:

`ops/daily-brief-runs/YYYY-MM-DD.json`

The date is always Asia/Shanghai.

The log is operational metadata only and must never be rendered into the Daily Brief article or spoken edition.

Recommended fields:

```json
{
  "date": "YYYY-MM-DD",
  "status": "started|research_complete|handoff_complete|failed",
  "started_at": "ISO-8601 timestamp",
  "updated_at": "ISO-8601 timestamp",
  "research_complete": false,
  "written": {
    "repo": "tangkk/daily_brief",
    "path": "_drafts/YYYY-MM-DD-daily-brief.md",
    "commit_sha": null,
    "readback_verified": false
  },
  "spoken": {
    "repo": "tangkk/lobster-daily-podcast",
    "path": null,
    "commit_sha": null,
    "readback_verified": false
  },
  "failure_stage": null,
  "failure_detail": null
}
```

Rules:

1. Create/update the log as the first GitHub side effect of each scheduled run, before the expensive research/publishing work.
2. Update it after research completes, after each canonical artifact commit, and after GitHub main read-back verification.
3. `handoff_complete` is allowed only when both canonical artifacts have been read back from GitHub main and verified.
4. On any failure, update the same dated log with `status: failed`, `failure_stage`, and a concise factual `failure_detail` whenever GitHub remains reachable.
5. Retrying the same date updates the same log and the same canonical artifacts; do not create duplicate run logs or duplicate Daily Brief/spoken files.
6. These logs are internal operations data and must not be referenced in published written or spoken content.

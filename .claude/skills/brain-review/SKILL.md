---
name: brain-review
description: Run a Second Brain review at the level that was asked for, meaning the daily note, the weekly, the monthly or the yearly. Use when the user says "daily", "daily note", "weekly review", "monthly review", "yearly review" (or the same in their own language), wants to log events or tasks for today, or wants to close out a week, a month or the year.
---

# Brain Review

Journal notes and reviews at four levels. Canonical workflow:
[reviews.md](../../../00-system/workflows/reviews.md), which holds every
step; this file only lists what gets skipped most. Templates:
`00-system/templates/{daily,weekly,monthly,yearly}.md`. The workflow doc
wins on any conflict with this file.

Pick the level from what was asked. **Each level reads the one below it**,
so when several are due they run in order in one session, never in
parallel.

- **Daily** (`02-journal/daily/YYYY-MM-DD.md`): cheap and unpolished.
  Durable content also goes to its canonical file or the inbox. A past
  daily is never rewritten; a late fact goes at its end under
  `## Added later`.
- **Weekly** (`02-journal/weekly/YYYY-Www.md`): the step that gets skipped
  is **the due evaluations** in `00-system/learning/organization-log/`.
  Every open `Result:` whose review date has arrived gets a verdict (keep,
  modify, revert) or a concrete new date.
- **Monthly** (`02-journal/monthly/YYYY-MM.md`): the steps that get skipped
  are the system health pass (`/brain-system check`, then `judge`) and
  **thinning the month's file** in `00-system/learning/observations/`. In
  the monthlies written in January, April, July and October, also the
  quarterly look outside.
- **Yearly** (`02-journal/yearly/YYYY.md`): includes the system
  retrospective against the year's files in
  `00-system/learning/organization-log/`.

When done, commit (and in multi-session mode: follow the pull-request rule
in AGENTS.md).

The daily, weekly and monthly levels can also run unattended every morning
([automation](../../../00-system/workflows/automation.md)). A reconstructed
day is not a day's record: it keeps the journal from being empty, it does
not replace capturing during the day.

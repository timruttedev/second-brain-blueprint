---
name: brain-review
description: Run a Second Brain review at the level that was asked for, meaning the daily note, the weekly, the monthly or the yearly. Use when the user says "daily", "daily note", "weekly review", "monthly review", "yearly review" (or the same in their own language), wants to log events or tasks for today, or wants to close out a week, a month or the year.
---

# Brain Review

Journal notes and reviews at four levels. Canonical workflow:
[reviews.md](../../../00-system/workflows/reviews.md). Templates:
`00-system/templates/{daily,weekly,monthly,yearly}.md`. The workflow doc
wins on any conflict with this file.

Pick the level from what was asked. **Each level reads the one below it**,
so when several are due they run in order in one session, never in
parallel. Journal files are history: append, and correct with a dated line,
never rewrite a past day.

## Daily

`02-journal/daily/YYYY-MM-DD.md`, created from the template when missing,
empty sections skipped. Append events, captures and tasks to the right
section. Dailies are cheap and unpolished. Durable content mentioned here
also goes to its canonical file (or to the inbox), so it does not live only
in the daily.

## Weekly

`02-journal/weekly/YYYY-Www.md`. Triage the inbox first, then condense this
week's dailies (condense, do not copy), walk the active projects for
progress, blockers and stagnation, check `00-system/indexes/todos.md`, and
update `00-system/current-context.md`.

**The step that gets skipped: the due evaluations** in
`00-system/learning/organization-log/`. Every entry whose `Result:` is still
open and whose review date has arrived gets a verdict (keep, modify,
revert) or a concrete new date. A permanently open `Result:` is not a valid
state; `linkcheck.py` reports it once the date has passed.

## Monthly

`02-journal/monthly/YYYY-MM.md`. Read the month's weeklies, look for the
larger patterns (recurring themes, where attention actually went, projects
to archive or recommit to), check the goals, then run the system health pass
via `/brain-system check`, promote confirmed observations to
`00-system/learning/patterns.md`, and pick at most one or two items from the
optimization backlog.

**The second step that gets skipped: thinning the month's observations.**
Everything promoted, resolved or clearly stale leaves
`00-system/learning/observations/YYYY-MM.md`, each with one line saying
where it went. Git keeps what was removed.

## Yearly

`02-journal/yearly/YYYY.md`: long-term development from the monthlies,
major decisions and their outcomes, goal retrospective, plus the system
retrospective against `00-system/learning/organization-log.md`.

## Automation

The daily, weekly and monthly levels can also run unattended as a scheduled
cloud routine, each step skipped when its output already exists
([automation](../../../00-system/workflows/automation.md)). A reconstructed
day is not a day's record: the routine keeps the journal from being empty,
it does not replace capturing during the day.

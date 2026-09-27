# Workflow: Reviews

Purpose: condense information upward **and** inspect the system itself.
Each level looks for changes, recurring themes, open loops, stagnating
projects, decisions, new or obsolete goals, patterns, and possible
structural improvements of the Second Brain.

Templates: `00-system/templates/{daily,weekly,monthly,yearly}.md`.
Files: `02-journal/daily/YYYY-MM-DD.md`, `02-journal/weekly/YYYY-Www.md`,
`02-journal/monthly/YYYY-MM.md`, `02-journal/yearly/YYYY.md`.

Journal files are history. An existing weekly, monthly or yearly means that
period is done. An existing daily is never rewritten; a fact that turns up
later is appended at its end under `## Added later`. Corrections happen in
canonical files, not by rewriting the past.

When you are done, commit (and in multi-session mode: follow the
pull-request rule in [AGENTS.md](../../AGENTS.md)).

## Daily

Capture and events. Cheap, unpolished, optional. No synthesis required.

## Weekly

1. Triage the inbox ([triage.md](./triage.md)). **Skipped when the weekly
   runs unattended**: the nightly triage owns the inbox then, and two runs
   filing the same capture would collide.
2. Read this week's dailies; write the weekly from them (condense, do not
   copy).
3. Walk the active projects: progress, blockers, stagnation → update the
   project files and [the projects index](../indexes/projects.md).
4. Update [`current-context.md`](../current-context.md) (focus, loops,
   recent decisions).
5. Work off the **due evaluations** in the month files of
   [`organization-log/`](../learning/organization-log/): every entry
   whose `Result:` is still open and whose review date has arrived gets its
   verdict (keep / modify / revert), or a concrete new date when there is
   genuinely no evidence yet. `linkcheck.py` reports overdue entries.
6. One-minute system check: anything for the current month's file in
   [`observations/`](../learning/observations/)?

## Monthly

1. Read this month's weeklies; write the monthly.
2. Look for larger patterns: recurring themes, where attention actually
   went, projects to archive or recommit to, areas emerging from usage.
3. Goals: progress, obsolescence (mark superseded, keep history).
4. **System health pass**: walk
   [system-health-check.md](./system-health-check.md) against the
   [`system-health.md`](../learning/system-health.md) criteria, then the
   judgment questions of [optimize.md](./optimize.md). Promote confirmed
   observations to [`patterns.md`](../learning/patterns.md). Pick at most
   1 to 2 items from
   [`optimization-backlog.md`](../learning/optimization-backlog.md) whose
   condition is met.
5. **Thin out the month's observations** (the month's file in
   [`observations/`](../learning/observations/)). Everything promoted,
   resolved, or clearly stale leaves the file, each with one line saying
   where it went.
   Close the due evaluations, as in the weekly.
6. **Quarterly: look outside.** In the monthly reviews written in January,
   April, July and October (covering December, March, June and September),
   run
   [the "Look outside" section](./optimize.md#look-outside-once-a-quarter)
   of `optimize.md`. Its output is at most three backlog entries, never a
   change.

Why steps 4 to 6 live here and not only in a routine prompt: a step that
only a scheduled prompt knows is invisible to the skills, the workflows and
every manual review.

## Yearly

1. Read the monthlies; write the yearly: long-term development, major
   decisions and their outcomes, goal retrospective, themes for next year.
2. System retrospective: did organization changes pay off
   (the year's files in
   [`organization-log/`](../learning/organization-log/))? What should
   evolve next year?

## Automation

The daily, weekly and monthly reviews can run by themselves every morning
as **one** scheduled routine. Setup, the catch-up windows, the heartbeat and
an example prompt are in [automation.md](./automation.md). The daily
catch-up covers the **7 days before today**, never today itself.

### Journal days are local days

Journal file names use the owner's local calendar (`<TIMEZONE>`), while
cron and Git often use UTC. When reconstructing a day from Git, convert
before filtering:

```bash
TZ=<TIMEZONE> git log --no-merges --date=format-local:'%Y-%m-%d %H:%M' --format='%ad %h %s'
```

Why: `git log --since/--until` compares against author dates, which may
carry mixed time zone offsets. A commit shortly after local midnight belongs
to the next journal day.

### A reconstructed day is not a protocol

What never reached the repository cannot be recovered from Git. An
automated daily note keeps the journal from being empty; it does not
replace capturing during the day. It says at the top that it was written
after the fact. **A day with no evidence gets no file**: an empty "nothing
happened" note would claim a record that does not exist. Never invent.

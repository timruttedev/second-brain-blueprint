# Workflow: Reviews

Purpose: condense information upward **and** inspect the system itself.
Each level looks for changes, recurring themes, open loops, stagnating
projects, decisions, new or obsolete goals, patterns, and possible
structural improvements of the Second Brain.

Templates: `00-system/templates/{daily,weekly,monthly,yearly}.md`.
Files: `02-journal/daily/YYYY-MM-DD.md`, `02-journal/weekly/YYYY-Www.md`,
`02-journal/monthly/YYYY-MM.md`, `02-journal/yearly/YYYY.md`.

Journal files are immutable history: an existing file means that period is
done. Corrections happen in canonical files, not by rewriting the past.

## Daily

Capture and events. Cheap, unpolished, optional. No synthesis required.

## Weekly

1. Triage the inbox ([triage.md](./triage.md)).
2. Read this week's dailies; write the weekly from them (condense, do not
   copy).
3. Walk the active projects: progress, blockers, stagnation → update the
   project files and [the projects index](../indexes/projects.md).
4. Update [`current-context.md`](../current-context.md) (focus, loops,
   recent decisions).
5. Work off the **due evaluations** in
   [`organization-log.md`](../learning/organization-log.md): every entry
   whose `Result:` is still open and whose review date has arrived gets its
   verdict (keep / modify / revert), or a concrete new date when there is
   genuinely no evidence yet. `linkcheck.py` reports overdue entries.
6. One-minute system check: anything for
   [`observations.md`](../learning/observations.md)?

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
5. **Thin out the month's observations.** Everything promoted, resolved, or
   clearly stale leaves the log, each with one line saying where it went.
   Close the due evaluations, as in the weekly.
6. **Quarterly (March, June, September, December): look outside.** Run
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
   ([`organization-log.md`](../learning/organization-log.md))? What should
   evolve next year?

## Automation

The daily, weekly and monthly reviews can run by themselves every morning
as **one** scheduled routine. Setup, the catch-up windows, the heartbeat and
an example prompt are in [automation.md](./automation.md).

Why one routine and not three: the weekly reads the dailies and the monthly
reads the weeklies, so they must run in order and in one session. Parallel
routines would race on the same repository.

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
after the fact, and a day with no evidence gets a short entry saying so.
Never invent.

# Learning Layer

How the system learns to organize itself better, not just what it stores.
The process is described in [learning-loop.md](../workflows/learning-loop.md).

| File | Role | Lifetime |
|---|---|---|
| [`observations.md`](./observations.md) + `observations/YYYY-MM.md` | Raw signals: friction, repeated searches, corrections. Signpost plus one file per month | Short-lived; thinned when promoted or stale |
| [`patterns.md`](./patterns.md) | Confirmed patterns with evidence (about 3 occurrences or an explicit owner confirmation) | Durable |
| [`organization-log.md`](./organization-log.md) + `organization-log/YYYY-MM.md` | Significant structural changes with reason and result. Signpost plus one file per month | Permanent, append-only |
| [`optimization-backlog.md`](./optimization-backlog.md) | Improvement ideas deliberately not done yet | Until done or discarded |
| [`system-health.md`](./system-health.md) | Criteria for judging the system's own quality | Durable, evolvable |

Flow: observation, then (if it repeats) pattern, then hypothesis and a
low-risk change, then an organization-log entry, then an evaluation at
review time.

## Why the two logs are split by month

- `observations.md` and `organization-log.md` stay at their paths as entry
  points. They hold the format and the month table, no entries.
- New entries go into the file for the current month. Create it if it does
  not exist yet, and add it to the table.
- Search the whole folder, not just the current month, because a repetition
  often sits in the previous month:
  `rg "<keyword>" 00-system/learning/observations/`.
- Why: append-only logs grow fast. One file per month keeps each file small
  enough to load, while the signpost keeps the path stable for links.

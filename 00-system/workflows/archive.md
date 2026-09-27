# Workflow: Archive

Purpose: retire finished or dead content without losing it. **Archive before
delete**, always.

1. **Confirm it is archivable**: finished project, obsolete area, superseded
   resource, person no longer connected to anything active. Decisions are
   never moved out of `07-decisions/`: they are history already.
2. **Extract durable knowledge first.** If something reusable is buried
   inside, move it to `06-knowledge/`, then archive the rest.
3. **Move** to `09-archive/`, mirroring the source path
   (`03-projects/x.md` → `09-archive/projects/x.md`).
4. **Mark it**: set `status: archived` and `archived: YYYY-MM-DD` (the day
   of the move) in the frontmatter, and add one dated line at the top saying
   why (finished, abandoned, superseded by ...).
5. **De-register**: remove it from indexes and
   [`current-context.md`](../current-context.md); update inbound links
   (point them at the archive path or annotate "(archived)").
6. **Log** significant archival (a whole area, many files) in the current
   month's file in [`organization-log/`](../learning/organization-log/).

Deleting user content requires an explicit owner request. Processed inbox
captures are the one exception: they are deleted after filing, because
their content already lives canonically and Git keeps the raw text
([triage.md](./triage.md)). Git history is
the safety net behind the archive, not a substitute for it. Un-archiving is
cheap: move it back and re-index.

# System Health

Criteria the system uses to judge its own quality. Checked briefly at the
monthly review, spot-checked at the weekly. A red criterion is an
observation; repeated red is a pattern that demands a fix. The procedure is
in [system-health-check.md](../workflows/system-health-check.md).

| Criterion | Healthy | Warning sign |
|---|---|---|
| Inbox size | Trends toward empty after reviews | More than 20 items, or items older than about 2 weeks |
| Stale projects | Active index matches reality | Projects untouched for months still listed as active |
| Duplicates | One canonical location per fact | The same information maintained in 2 or more places |
| Contradictions | Current facts are consistent | Two files disagree about the current state |
| Orphaned files | Everything reachable via index, links or an obvious location | Files nothing references and search will not surface |
| Oversized files | Files stay skimmable | A file so long agents load it in chunks (roughly over 500 lines): split it, unless it is a verbatim source that says so in its header |
| Dead categories | Every folder earns its existence | Empty or near-empty folders untouched for months |
| Folder depth | Mostly 3 levels or fewer below the root | Deep nesting needed to reach content |
| Retrieval failures | Questions answered via context, index, file | Repeated wrong guesses or multi-step hunts for the same information |
| Instruction size | AGENTS.md, CLAUDE.md and rules stay lean | Agent instructions ballooning; CLAUDE.md near 200 lines |
| Metadata usage | Every frontmatter field is actually used | Fields set but never queried: remove them |
| Type sprawl | Taxonomy small and meaningful | Types or tags nobody retrieves by |
| Template fit | Templates reduce work | Sections routinely deleted or left empty |
| Internal links | Links resolve (`linkcheck.py` exits 0) | Broken links after moves: the "update references" step was skipped |
| Index freshness | Indexes match reality | Index entries pointing at archived or renamed files |
| Checks alive | The canary is reported, scheduled runs update their heartbeat | A check that reports green without proof it ran |
| Open evaluations | Organization-log results get a verdict or a date | `linkcheck.py` reports due evaluations |

Findings go to [observations.md](./observations.md); structural fixes
follow [reorganization.md](../workflows/reorganization.md).

The mechanical part runs with one command:

```bash
python3 00-system/scripts/linkcheck.py --orphans
```

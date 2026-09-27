# Workflow: Reorganization

Purpose: change the structure of this repository safely. Structure is
evolvable; knowledge is not expendable. **No reorganizing for its own
sake**: every change needs a concrete benefit against the optimization
priorities in [AGENTS.md](../../AGENTS.md) (retrieval first, aesthetics
never).

## Low-risk changes: do them autonomously

Moving or renaming files, creating folders, merging near-empty folders,
splitting an oversized file or a too-broad category, consolidating redundant
AI-generated content, adding or removing indexes, improving templates and
workflows, simplifying metadata, fixing links, archiving inactive content.

Checklist, even for low-risk moves:

1. State (to yourself) the concrete benefit.
2. Make the change.
3. **Update all references**: search for the old path or name across the
   repository (`rg "old-name"`) and fix every link, index entry and mention.
4. Run `python3 00-system/scripts/linkcheck.py --orphans`; it must exit
   clean.
5. Commit with a message that says what and why.

## Significant changes: extra care

Anything touching the top-level layout, the taxonomy, many files at once, or
established conventions:

1. Consider parking it in
   [`optimization-backlog.md`](../learning/optimization-backlog.md) first.
   Is the evidence (patterns, not one-off ideas) actually there?
2. Execute traceably: one logical change per commit.
3. Update every reference (step 3 above, thoroughly).
4. Add an entry to [`organization-log.md`](../learning/organization-log.md)
   (Observation / Change / Reason / Result with a review date / Reversible).
5. Review the Git diff before committing: **is any information lost?**
   Moved is not lost; deleted content must reappear elsewhere or in
   `09-archive/`. A quick check for removed lines:
   `git diff --cached | grep "^-" | grep -v "^--- "`.
6. Update [architecture.md](../architecture.md) if the described state
   changed.

## Never without explicit owner consent

Deleting important historical user information, irreversibly deleting raw
notes, mass destructive cleanup, sending confidential content to external
systems, changing external systems, storing secrets.

**Archive before delete**: move to `09-archive/` (mirroring the source
location) instead of removing ([archive.md](./archive.md)). Git history is
the safety net behind that, not a substitute for it.

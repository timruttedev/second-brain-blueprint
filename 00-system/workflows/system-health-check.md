# Workflow: System Health Check

Purpose: a mechanical quality pass against the criteria in
[`system-health.md`](../learning/system-health.md). Run it at the monthly
review, or on request. Cheap checks first.

1. **Inbox**: count items and the age of the oldest capture
   (`ls 01-inbox/`).
2. **Indexes vs. reality**: entries pointing at moved, archived or missing
   files; active things missing from indexes.
3. **Staleness**: "active" projects with old `updated:` dates or no recent
   Git activity.
4. **Links, anchors, orphans, frontmatter and line budgets.** Run the
   script, do not grep:

   ```bash
   python3 00-system/scripts/linkcheck.py --orphans
   ```

   - **Exit 1**: a link, an `#anchor`, a `type:`, a `status:`, a
     frontmatter field name or a code fence does not resolve, a file has
     outgrown its own `max_lines`, or an evaluation in the organization log
     is due. Fix these immediately; a broken link is usually a rename whose
     inbound references were missed.
   - **Orphans** are a hint, not an error: a content file nothing links to
     is unreachable in practice, so link it from its area README or an
     index.
   - **Exit 2 means the check itself is broken**, not the repository. The
     script carries a canary, [`canary.md`](../scripts/canary.md), holding
     one deliberately broken link that every full run **must** find. If it
     does not, the script stops with exit 2 instead of reporting "0
     findings". Fix the script, never the canary. Why: a check that
     silently reports green is worse than no check.
   - **"Code fence never closed"** is the second half of that guard. An
     unclosed fence hides everything after it from the check. Usually the
     culprit is a prose line that happens to start with three backticks.
   - **`type:`, `status:` and field names** are compared against
     [taxonomy.md](../taxonomy.md), inside the frontmatter only. A hit is
     not a licence to invent a value: a new value goes into the taxonomy
     first (with a stated retrieval benefit) and into the script second.
     Why: invented values look plausible, and nothing else complains.
   - **`max_lines`**: a file may declare its own line budget in
     frontmatter (for example `current-context.md`, the entry point of
     every session). A hit is not a licence to raise the number: first cut
     what the file duplicates from elsewhere.
   - Do not replace the script with an ad-hoc grep. Its rules for anchors,
     placeholders and inline code are tested; a grep is not.
5. **Oversized files**: anything over about 500 lines outside the journal
   is a split candidate (`wc -l` over tracked `.md` files).
   *Exempt: primary sources.* A verbatim record (chat log, transcript,
   contract wording) is not split, because every cut would be arbitrary.
   Such a file states the exemption in its own header and points to the
   working document that is read instead. Check that the note is there; do
   not re-propose the split.
6. **Dead categories**: folders empty or untouched for months.
7. **Duplicates and contradictions**: grep for the same fact stated in
   several canonical files.
8. **Instruction size**: are AGENTS.md, CLAUDE.md and `.claude/rules/`
   growing? CLAUDE.md must stay well under 200 lines.
9. **Metadata that nobody queries**: a documented field that is set but
   never used for retrieval is a removal candidate. `linkcheck.py` already
   checks that values are valid; whether a field is ever queried is a
   judgment question, so this step stays manual: for each documented
   field, can you name a search, index or script that uses it?

10. **Generated figures still match their source** (only if you have
    scripts that generate files): run their check mode and regenerate on
    drift. A large diff means the source changed, and that is the real
    finding.
11. **Scheduled routines actually reach this repository** (only if you use
    [automation.md](./automation.md), and only in a session that can list
    routines):
    - Each routine's last run succeeded and is recent enough for its
      schedule.
    - The run's session shows this repository as a source. **An empty
      source list means the run had no checkout and did nothing**, while
      still reporting success.
    - Its heartbeat in `00-system/sync/state/automation-runs.json` is fresh.
      The heartbeat commit is the proof, not the routine status.
    - Every file path its prompt names still exists. The prompts live
      outside the repository, so a rename here breaks them silently.

## Output

- Fix trivial findings immediately (broken links, index rot).
- Everything else → the current month's file in
  [`observations/`](../learning/observations/) (dated), structural fixes via [reorganization.md](./reorganization.md),
  bigger ideas → [`optimization-backlog.md`](../learning/optimization-backlog.md).

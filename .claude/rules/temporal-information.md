# Rule: Temporal Information

How to handle facts that change over time.

- **Distinguish current state from historical state.** The newest explicit
  owner statement defines current state. Earlier values remain as dated
  history.
- **When a value changes,** update the current statement in place and keep
  a short dated history line, for example
  `2026-01-01: A → 2026-06-01: B`. For trivial values, Git history alone
  may be enough. Anything the owner might ask "since when?" or "why did
  this change?" about gets an inline history note.
- **Corrected assumptions are marked corrected, not erased.**
- **Date things.** Undated "current" facts rot. The `updated:` frontmatter
  field and dated history lines prevent that.
- **Current means dated, not flagged.** Do not mark a file `status: current`.
  Why: nobody resets an undated flag, so it turns false silently. Use
  `updated:` and dated history instead.
- **Journal files are immutable history.** Corrections happen in canonical
  files, not by rewriting the past.

# Rule: Organization

When and how the structure of the repository may change.

- **Structure is evolvable.** Follow the
  [reorganization workflow](../../00-system/workflows/reorganization.md).
  Reorganize only for a concrete benefit.
- **Priorities:** retrieval > context speed > fewer duplicates > low
  maintenance > cheap capture > small AI contexts > machine readability >
  human readability > simplicity. Never reorganize for aesthetics, tag
  volume or ontological perfection.
- **After any move or rename:** `rg` for the old path and name, and fix
  every reference (links, indexes, mentions) in the same commit. Then run
  the [link checker](../../00-system/scripts/linkcheck.py).
- **Log significant structural changes** in
  [organization-log.md](../../00-system/learning/organization-log.md). When
  the described state changes, update
  [architecture.md](../../00-system/architecture.md) in the same change.
- **Structure follows complexity.** One file until it actually grows. No
  preemptive folders, no empty categories.
- **Frontmatter follows the [taxonomy](../../00-system/taxonomy.md).** New
  fields only with a stated retrieval or automation benefit.

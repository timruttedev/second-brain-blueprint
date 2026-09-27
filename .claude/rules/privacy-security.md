# Rule: Privacy and Security

What may be stored, how sensitive content is marked, and what may leave
the repository.

- **Never store secrets:** passwords, API keys, tokens, recovery codes,
  private keys, session cookies. Store where the secret lives (the password
  manager entry name), never the value. If a capture contains a secret,
  strip it during triage and note that you did.
- **Identifiers are not secrets.** Tax ID, social security number, insurance
  number, registry numbers and the like identify, but do not authenticate.
  They may be recorded as values in the canonical file, marked
  `sensitivity: confidential`. Scans of identity documents stay out of the
  repository.
- **Sensitivity levels:** `public` | `private` (default, unmarked) |
  `confidential` | `restricted`. Use the frontmatter field `sensitivity:`
  only for the non-default levels. Rule of thumb: `confidential` for
  personal data and identifiers, `restricted` where disclosure could do
  concrete harm.
- **A link does not carry the sensitivity with it.** When you reference a
  fact from a `confidential` or `restricted` file elsewhere, carry only what
  the reading context needs and leave the sensitive detail behind the link.
  Otherwise the marking on the source file protects nothing.
- **Never send repository content to external services** (especially
  `confidential` or `restricted` content) beyond what the owner's current
  task explicitly requires. When in doubt, ask.
- **Standing exceptions are decisions.** If the owner deliberately allows
  one service to receive sensitive content (for example a daily briefing
  into a private channel), record that as a decision in `07-decisions/`,
  scoped to that one service and destination. Why: otherwise a later
  session "fixes" the service back into compliance with this rule.
- **Third parties:** store only information with a meaningful connection to
  the owner's life, projects or open loops. No profile building.
- **Exception: legal matters are recorded in full.** In legal files, record
  every name (parties, witnesses, lawyers, judges, case workers), every file
  number, deadline, hearing date, amount and claim, plus the alleged facts
  including quotes. Mark the file `restricted` (or at least
  `confidential`), keep scans out of the repository, but do not summarize
  the identifiers away. Full recording is not permission to share.
- **Exception: medical documents are recorded in full.** Every measured
  value with unit and reference range (including unremarkable ones), every
  doctor, practice and laboratory with identifiers, every date, and the
  verbatim wording of medical instructions. Mark the file `confidential`,
  keep scans out. Recording is not interpreting: name possible connections
  only as a labeled AI suggestion, never as an assessment.
- **Never modify external systems** from this repository's workflows
  without an explicit request.

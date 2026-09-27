# Rule: Privacy and Security

The specifics behind the privacy section of
[AGENTS.md](../../AGENTS.md#privacy-and-security).

- **Secrets in a capture** (passwords, API keys, tokens, recovery codes,
  private keys, session cookies): strip them during triage and note that
  you did. Keep where the secret lives (the password manager entry name).
- **Identifiers are not secrets.** Tax ID, social security number,
  insurance number, registry numbers identify but do not authenticate. They
  may be recorded in the canonical file, marked `sensitivity: confidential`.
  Scans of identity documents stay out of the repository.
- **Which level:** `confidential` for personal data and identifiers,
  `restricted` where disclosure could do concrete harm. Write
  `sensitivity:` only for non-default levels.
- **A link does not carry the sensitivity with it.** When you reference a
  fact from a `confidential` or `restricted` file elsewhere, carry only what
  the reading context needs and leave the detail behind the link.
  Otherwise the marking on the source file protects nothing.
- **Standing exceptions are decisions.** If the owner lets one service
  receive sensitive content (for example a daily briefing into a private
  channel), record it in `07-decisions/`, scoped to that service and
  destination. Why: otherwise a later session "fixes" the service back into
  compliance.
- **Never modify external systems** from this repository's workflows
  without an explicit request.
- **Fuller recording is opt-in.** Recording medical documents or legal
  matters in full is not a default; the owner can switch it on
  ([optional policies](../../00-system/optional-policies.md)).

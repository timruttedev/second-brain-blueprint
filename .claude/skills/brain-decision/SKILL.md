---
name: brain-decision
description: Record a durable decision in the Second Brain, or supersede an old one. Use when the user has decided something ("I've decided", "we're going with X", "X no longer applies, now it's Z", or the same in their own language), so the system can later answer "why did I choose this back then?".
---

# Brain Decision

Decision records that still explain themselves in years. Canonical workflow:
[decision-record.md](../../../00-system/workflows/decision-record.md).
Template: [decision.md](../../../00-system/templates/decision.md). The
workflow doc wins on any conflict with this file.

- Record only decisions the owner actually made or confirmed. An AI
  recommendation is not a decision; if you must record one, use
  `status: proposed` and say whose it is.
- New record: `07-decisions/YYYY-MM-DD-slug.md` with context, reasons and
  alternatives, written now, while the reasons are fresh.
- Replacing an earlier decision: mark the old one `superseded` with a dated
  link to the new one (never delete or rewrite it), and link back from the
  new one.
- Register it in `00-system/indexes/decisions.md`, link it from the
  affected project or area, and update `00-system/current-context.md` if it
  shapes the current focus.

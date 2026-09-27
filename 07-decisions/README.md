# 07-decisions

Durable decision records. Long-term purpose: answer *"why did I decide that
back then?"*

- File name: `YYYY-MM-DD-short-slug.md`; template:
  [decision.md](../00-system/templates/decision.md).
- Contains: date, status, context, decision, reasons, alternatives,
  consequences, later changes.
- **Never delete a decision.** When replaced: set `status: superseded` and
  add a dated note linking the new record. Reverted decisions keep their
  record too.
- Recent and high-impact decisions are listed in
  [the decision index](../00-system/indexes/decisions.md).
- Record decisions that are durable and non-obvious, not every trivial daily
  choice.
- Workflow: [decision-record](../00-system/workflows/decision-record.md).

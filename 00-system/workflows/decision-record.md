# Workflow: Decision Record

Purpose: record a durable decision so the system can answer *"why did I
decide that back then?"* years later, from the record alone.

1. **Only real decisions.** An AI recommendation or a passing thought is not
   a decision: ask for, or wait for, the owner's explicit choice. Trivial
   everyday choices need no record.
2. **Check `07-decisions/`** for an existing decision on the same question.
   - New question → new record `07-decisions/YYYY-MM-DD-short-slug.md` from
     [the decision template](../templates/decision.md). Capture context,
     reasons and alternatives **now**, while they are fresh: they are the
     point of the record.
   - Replaces an old decision → create the new record, then mark the old one
     `status: superseded` with a dated link under "Later changes". Never
     delete or rewrite it. Link back from the new record.
3. **Register it**: one line in [the decisions index](../indexes/decisions.md);
   link it from the affected project or area ("Key decisions"); update
   [`current-context.md`](../current-context.md) if it shapes the current
   focus.

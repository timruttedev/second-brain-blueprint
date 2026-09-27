# Workflow: Learning Loop

Purpose: the system learns not just information but **how to organize
information better**. This is the continuous process behind
[`00-system/learning/`](../learning/README.md).

```
OBSERVE
   ↓
DETECT PATTERN
   ↓
FORM HYPOTHESIS
   ↓
MAKE LOW-RISK IMPROVEMENT
   ↓
USE SYSTEM
   ↓
EVALUATE
   ↓
KEEP / MODIFY / REVERT
```

## Stages

1. **OBSERVE**: during normal work, note friction and signals in the
   current month's file in
   [`observations/`](../learning/observations/) (create it and add it to
   the table in [the signpost](../learning/observations.md) if it is
   missing): repeated searches for
   the same thing, two categories always needed together, a template causing
   busywork, a kind of information that keeps getting misfiled, the owner
   correcting the same assumption again. Cheap, dated one-liners. Not every
   observation becomes a rule.
2. **DETECT PATTERN**: when an observation repeats (rule of thumb: about 3
   independent occurrences) or the owner confirms it explicitly, consolidate
   it into [`patterns.md`](../learning/patterns.md) with its evidence.
3. **FORM HYPOTHESIS**: "If we change X, retrieval, capture or maintenance
   improves because Y." Write it with the pattern or as a backlog entry.
4. **MAKE LOW-RISK IMPROVEMENT**: prefer the smallest reversible change (an
   index tweak before a folder restructure). Larger ideas wait in
   [`optimization-backlog.md`](../learning/optimization-backlog.md). Follow
   [reorganization.md](./reorganization.md).
5. **USE SYSTEM**: let real usage accumulate. No second change on top of an
   unevaluated one in the same spot.
6. **EVALUATE**: every structural change gets a **review date** in its
   entry in the current month's file in
   [`organization-log/`](../learning/organization-log/), written as
   `Result: _open, review on YYYY-MM-DD: <what to check>._`. The
   weekly review works off every entry whose date has arrived: did the
   friction disappear? Check against
   [`system-health.md`](../learning/system-health.md).
7. **KEEP / MODIFY / REVERT**: record the verdict in the entry's `Result:`
   field. Reverting a failed change is success: that is the system learning.

A permanently empty `Result:` is not a valid state. `linkcheck.py` reports
an evaluation once its review date has passed, or 30 days after an entry
without a date. Why: without a mechanical reminder, evaluations pile up and
the loop stops at step 5.

## What feeds the loop

Triage friction, retrieval failures, review findings, explicit owner
corrections and repeated preferences, health checks, and (once a quarter)
a look at outside practice ([optimize.md](./optimize.md#look-outside-once-a-quarter)).

## Keep the working memory small

Observations are working memory, not an archive. The monthly review thins
the month's file: everything promoted to a pattern, resolved, or clearly
stale leaves it, each with one line saying where it went. Git keeps what was
removed.

## Guardrails

- Evidence before rules.
- One change at a time per zone.
- Everything significant is logged.
- Knowledge is never lost to a structure experiment
  (see [reorganization.md](./reorganization.md)).
- A rule that no mechanism checks tends not to hold. When a rule keeps
  breaking, prefer adding a check (a script, a linkcheck rule) over
  rewording the rule.

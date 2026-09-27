---
name: brain-system
description: The Second Brain working on itself, meaning persist what a session learned, check the system's health, judge the whole structure, or carry out a structural change. Use when the user corrects an assumption or states a lasting preference, at the end of a substantial session, when they ask "how healthy is the system", "check the brain", ask to optimize or improve the system, or ask to restructure, move, rename, split, merge or archive something.
---

# Brain System

Four modes, one skill, because they are one loop: **learn** records the
signal, **check** measures it mechanically, **judge** decides what it means,
**change** carries it out. Say which mode you are in.

Canonical workflows, each of which wins over this file:
[learning-loop](../../../00-system/workflows/learning-loop.md),
[system-health-check](../../../00-system/workflows/system-health-check.md),
[optimize](../../../00-system/workflows/optimize.md),
[reorganization](../../../00-system/workflows/reorganization.md) and
[archive](../../../00-system/workflows/archive.md).

## learn

Watch for: explicit corrections, durable preferences, new decisions, new
recurring patterns, changes to existing facts, retrieval failures,
organization problems, obsolete rules. Persist at the RIGHT level. These are
gradations, not instant rules:

1. **Observation:** one dated entry in the current month's file in
   `00-system/learning/observations/` (create it and add it to the
   signpost table if missing). Single occurrences stop here; note repeat
   counts (2x, 3x).
2. **Repeated pattern** (about three occurrences, or explicit owner
   confirmation): `00-system/learning/patterns.md`, with the evidence.
3. **Stable knowledge:** the canonical file (knowledge, project, area,
   person), with dated history for changed facts. Decisions go to
   `07-decisions/` via `/brain-decision`.
4. **System rule**, only for durable, confirmed expectations: the smallest
   change in the right place (`.claude/rules/`, a workflow doc, a template),
   logged when significant.

A correction always fixes the canonical file NOW: current state updated,
history kept, wrong assumption marked corrected. The gradations only decide
whether it also becomes a pattern or a rule. Never store AI inference as the
owner's fact, and never let this become a chat archive.

## check

Follow [system-health-check](../../../00-system/workflows/system-health-check.md).
Mechanical first, with the script instead of a hand-made grep:

```bash
python3 00-system/scripts/linkcheck.py --orphans
```

**Exit 2 means the check is broken, not the repository** (the canary was
not found): fix the script, not the canary. Then walk the remaining steps
of the workflow against `00-system/learning/system-health.md`. Fix trivial
findings on the spot; the rest becomes a dated observation. Report a short
diagnosis: green, findings fixed, findings recorded.

## judge

The step back over the whole system, fed by `00-system/learning/`
(observations, patterns, system health) and the question checklist in the
optimize workflow: taxonomy fit, dead or oversized categories, duplicates,
template dead weight, instruction bloat, missing or useless indexes.

Low-risk improvements happen right away, under the **change** rules below.
Bigger or unclear ideas go to `00-system/learning/optimization-backlog.md`.
Evolution over revolution: one small improvement per real, evidenced
problem.

## change

Follow [reorganization](../../../00-system/workflows/reorganization.md)
(and [archive](../../../00-system/workflows/archive.md) for retiring
content). Only with a concrete benefit: retrieval, never aesthetics. The
short version: make the change, `rg` for the old path or name and fix
**every** reference, verify in the diff that nothing was lost, run
linkcheck, commit with what and why (and in multi-session mode: follow the
pull-request rule in AGENTS.md). Archive before delete, and never destroy
user content without explicit consent.

A significant change also gets an entry in the current month's file in
`00-system/learning/organization-log/`, with a dated result:
`_open, review on YYYY-MM-DD: <what to check>._` Why: a vague "check at the
next review" is never measured; `linkcheck.py` turns a passed date into a
finding.

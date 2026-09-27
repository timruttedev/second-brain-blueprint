---
name: brain-triage
description: Process the Second Brain inbox by classifying captures and moving them to their canonical homes (projects, areas, knowledge, decisions, journal, people). Use when the user says "triage", "process the inbox", "clean up the inbox" (or the same in their own language), or when the inbox has piled up.
---

# Brain Triage

Empty the inbox into canonical files. Canonical workflow:
[triage.md](../../../00-system/workflows/triage.md) (its questions, in
order; search before deciding). The workflow doc wins on any conflict with
this file. Related: [taxonomy](../../../00-system/taxonomy.md),
[create-project](../../../00-system/workflows/create-project.md),
[decision-record](../../../00-system/workflows/decision-record.md),
[archive](../../../00-system/workflows/archive.md).

**First step, before the inbox:**
`python3 00-system/scripts/branch_overview.py --fetch`.
Why: unmerged branches hold unprocessed work too, and finished work on a
branch is invisible to every later session. Nothing gets merged here, but a
file the script reports as a collision is not touched until you have read
the other branch.

Per capture:

1. Find the canonical home and update it. Create a new file only when no
   existing home makes sense.
2. Delete the processed capture. Git keeps the raw history.

Afterwards: update the touched indexes in `00-system/indexes/` and
`00-system/current-context.md`, and put notable friction into
`00-system/learning/observations.md`.

For ambiguous items, make a sensible call and say so. If an item is
genuinely undecidable, leave it in the inbox with a one-line note.

Report a compact summary: item -> destination.

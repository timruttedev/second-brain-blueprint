# Architecture

The current shape of the system and the reasons behind it.

> This file always describes the **current** state. When the structure
> evolves, update this file in the same change and log the move in the
> current month's file of the
> [organization log](./learning/organization-log.md).

Version: 1 (the structure version AGENTS.md refers to; raise it when the
top-level layout changes).

Where the system is meant to go (target state, not current):
[vision.md](./vision.md).

## Overview

A flat, numbered top level, ordered roughly by how often an agent should
look there first:

```
00-system/    control plane: how the system works and learns
01-inbox/     capture buffer, no filing decisions at write time
02-journal/   time-based notes: daily / weekly / monthly / yearly
03-projects/  outcome-driven, time-bounded work
04-areas/     ongoing responsibilities without an end date
05-people/    person records
06-knowledge/ reusable knowledge, separated from personal context
07-decisions/ append-mostly decision records
08-resources/ external reference material
09-archive/   inactive content, mirrored structure, preserved forever
```

## Why this shape

- **Numbered prefixes** give humans and agents a stable scan order and keep
  the control plane (`00-system`) at the top.
- **PARA-like split** (projects, areas, resources, archive) because the main
  retrieval question is "is this actionable now?", not "what topic is
  this?". Journal, people, decisions and knowledge get their own homes
  because they answer different questions: when, who, why, what.
- **Inbox as a directory of atomic files**, not one big file. Several
  devices and automations capture at the same time, and Git must merge
  without conflicts.
- **Markdown and Git only** as the knowledge base. No database, no
  proprietary format, no model-specific memory as source of truth. Any
  agent that can read files can operate the system. Git is history, sync
  and safety net.
- **Code is a tool, never a store.** `00-system/scripts/` holds Python for
  the few jobs where a reconstructed one-liner is a real risk (for example
  checking links and anchors). The script carries the logic, the Markdown
  next to it carries the knowledge, and anything a script writes must be
  reproducible from source data. Reading the repository must never require
  running a script.
- **Deliberately few subfolders.** Subcategories should emerge from real use
  (structure follows complexity), not be predicted up front.

## Stable vs. evolvable

**Stable (change only with explicit owner consent):**

- Markdown and Git as the canonical knowledge base.
- The [principles](./principles.md), especially: preserve knowledge, evolve
  structure; archive before delete; no secrets.
- The existence of a capture inbox, a control plane, decision records and an
  archive: the functions, independent of their current names.

**Evolvable (agents may change with a logged reason):**

- Folder names, numbering and nesting below the top level.
- The [taxonomy](./taxonomy.md) and metadata schema.
- Templates, indexes, workflows, skills.
- File naming conventions.
- The top-level layout itself, if evidence shows a better shape. That is a
  significant change: update every reference, log it, verify nothing was
  lost.

## Deliberately open

No speculative design for these. They get answered when usage demands it:

- **Which areas exist.** `04-areas/` starts empty. Areas are created when
  triage keeps routing captures to the same life domain.
- **Which knowledge topics get folders.** `06-knowledge/` starts flat.
- **Journal scaling** (per-year subfolders).
- **External storage for large attachments.** Decided when the first large
  file actually appears.
- **More indexes, metadata fields, taxonomy types.** Only with a
  demonstrated retrieval or automation benefit.
- **Hooks for session-end learning.** CLAUDE.md prescribes a manual check.
  Automate only if it proves robust and cheap. The system must never
  depend critically on a model-specific feature.

## Operating modes

The repository runs in **single-session mode** by default: one session at
a time, commits straight to `main`. **Multi-session mode** is opt-in and
gives every session its own worktree and branch, with a pull request per
task. The switch is one line in AGENTS.md
([operating mode](../AGENTS.md#operating-mode)). Why a default without
worktrees: most owners run one session at a time, and a branch plus pull
request for every logged workout is heavier than the work itself.

## Automation

Scheduled cloud runs can keep the system alive without a session: a
morning journal run (daily note, reviews when due) and a nightly inbox
triage. They commit directly to `main` in both operating modes, because
each run has its own isolated checkout. Each run writes a heartbeat,
because a run's status says nothing about its effect: only the heartbeat
commit proves the work happened.
Details: [automation workflow](./workflows/automation.md).

Ingest pipelines (mail, documents, voice notes) are optional. They drop
atomic captures into `01-inbox/` and triage takes it from there.

## Quality gates

- [linkcheck.py](./scripts/linkcheck.py) checks links, anchors, `type:`
  values, frontmatter fields, code fences, line budgets (`max_lines`) and
  due evaluations in the organization log.
- A [canary](./scripts/canary.md) (a deliberately broken link) proves the
  checker still finds problems. A checker that silently reports green is
  worse than none.
- [branch_overview.py](./scripts/branch_overview.py) shows work on branches
  that `main` does not have yet, so a session does not redo it
  (multi-session mode).
- The [pre-commit checks](../AGENTS.md#pre-commit-checks) run before every
  commit. CI (`.github/workflows/checks.yml`) runs the link checker and the
  script tests on every push and pull request.

## Key flows

- **Information lifecycle:** CAPTURE → INBOX → TRIAGE → CANONICALIZE →
  CONNECT → USE → REVIEW → ARCHIVE
  ([capture](./workflows/capture.md), [triage](./workflows/triage.md))
- **Retrieval:** question → current context → indexes → canonical file →
  related files → history ([retrieval](./workflows/retrieval.md))
- **Self-improvement:** OBSERVE → PATTERN → HYPOTHESIS → LOW-RISK CHANGE →
  USE → EVALUATE → KEEP / MODIFY / REVERT
  ([learning loop](./workflows/learning-loop.md))

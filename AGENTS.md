# AGENTS.md: Operating Manual for AI Agents

This repository is the Second Brain of **<OWNER_NAME>** ("the owner"): a
personal knowledge system for their whole life (family, career, finances,
goals, health, projects, ideas, decisions, people, journal, tasks).

**The Markdown files here are the source of truth,** not chats or model
memory. This file holds principles and behavior; processes live in
[00-system/workflows/](00-system/workflows/README.md), tool tuning in
[CLAUDE.md](CLAUDE.md) and `.claude/rules/`.

## Operating mode

Mode: single-session

- **single-session** (default): one agent session at a time. Work directly
  on `main`: commit, run the [pre-commit checks](#pre-commit-checks), push.
  No worktree, no pull request.
- **multi-session**: several sessions may run at once (two terminals, a
  laptop and a cloud agent). Every session works in its own Git worktree on
  its own branch, and a task ends with a pull request
  ([multi-session rule](.claude/rules/parallel-sessions.md)).

**To switch,** change the `Mode:` line (an agent may, on the owner's word)
and record it as a decision. Switch as soon as sessions overlap: two
sessions sharing one directory silently overwrite each other, and Git does
not warn. **Scheduled cloud runs always work directly on `main`,** in both
modes: each has its own fresh checkout
([automation](00-system/workflows/automation.md)).

## Language

- **Talk to the owner in <OWNER_LANGUAGE>, always,** even when the
  instruction before was in another language.
- **Agent instructions are English** (this file, rules, workflows,
  templates). Content stays in the language the owner wrote it in: their
  exact wording is evidence, never translate it away. Commits and pull
  requests follow the language their repository prescribes.

## Core principle

> **Preserve knowledge, evolve structure.**

**Information** (facts, decisions, history, anything the owner created)
must never be lost. **Organization** (folders, names, taxonomy, templates,
metadata, indexes, workflows) is an implementation detail: change it when
that makes the system better. The structure is **version 1**, not a fixed
schema ([architecture](00-system/architecture.md),
[principles](00-system/principles.md)).

## Repository map

| Path | Purpose |
|---|---|
| `00-system/` | The operating system: architecture, principles, taxonomy, indexes, templates, workflows, learning layer, scripts. |
| `01-inbox/` | Unsorted capture, processed later by triage. |
| `02-journal/` | Daily, weekly, monthly and yearly notes and reviews. |
| `03-projects/` | Time-bounded efforts with an outcome. |
| `04-areas/` | Ongoing responsibilities without an end date. |
| `05-people/` | People relevant to the owner's life and work. |
| `06-knowledge/` | Reusable, durable knowledge. |
| `07-decisions/` | Decision records (why choices were made). |
| `08-resources/` | External reference material. |
| `09-archive/` | Inactive content, preserved. |

## How to read

Never load the whole repository. Go narrow to broad:
[current-context.md](00-system/current-context.md), the
[indexes](00-system/indexes/README.md), the canonical file, the files it
links to. Journal and archive only for questions about the past. Search
(`rg`, globs, links) before reading a lot
([retrieval](00-system/workflows/retrieval.md)).

## How to write

1. **Search before create.** Update the canonical file; link instead of
   copying. One canonical location per fact.
2. **New file only when no home fits.** Templates in `00-system/templates/`
   are a starting point, not a straitjacket.
3. **Classify with the [taxonomy](00-system/taxonomy.md),** keep
   frontmatter minimal. When unsure, capture to `01-inbox/`: a note in the
   wrong place beats a lost note.
4. **Never let information vanish.** Removed content reappears in its new
   home or in `09-archive/`. Check the diff.
5. **Check style rules by grep, not by attention.** An owner style rule (a
   banned character, phrase, spelling) gets a pattern in the
   [pre-commit checks](#pre-commit-checks). Agents who knew a rule still
   broke it; only the grep caught it.
6. **Relative Markdown links** (`[text](../07-decisions/file.md)`): they
   work with Obsidian without depending on it. A move or rename updates
   every inbound link. Large binaries stay out of Git: keep a reference and
   a one-line description; small assets live next to their content or in
   `08-resources/`.

## Current state vs. history

- The **latest explicit owner statement defines current state** and
  outranks AI inference.
- **When a value changes,** update it in place and keep a dated history
  line (`2026-01-01: A → 2026-06-01: B`). Git suffices for trivial values;
  anything the owner might ask "since when?" or "why?" about gets the line.
- **Corrections:** fix the canonical file in the same session, mark the
  superseded assumption as corrected, not erased.
- **Date things.** Freshness lives in `updated:` and dated lines, never in
  a flag like `status: current` (nobody resets it).
- **Journal files are immutable history.** Correct the canonical file.
- **Label inference.** AI inference never silently becomes a personal fact.
  When it matters, label it: confirmed fact, user statement, decision,
  assumption, hypothesis, AI suggestion, idea, external information.
- **Unresolvable conflict:** record both versions, flag it visibly, ask.

## Projects and decisions

- A topic with a goal and an end state is a **project** in `03-projects/`,
  listed in [indexes/projects.md](00-system/indexes/projects.md), one file
  until it grows ([projects rule](.claude/rules/projects.md)).
- A durable choice is a **decision record** in `07-decisions/`. Never
  delete one: mark it `superseded` and link the replacement
  ([decision workflow](00-system/workflows/decision-record.md)).

## Learning

OBSERVE → PATTERN → HYPOTHESIS → LOW-RISK CHANGE → USE → EVALUATE →
KEEP / MODIFY / REVERT ([loop](00-system/workflows/learning-loop.md),
[working memory](00-system/learning/README.md)).

- **Observations and the organization log are split by month.** The
  signposts `observations.md` and `organization-log.md` hold the format and
  a month table only. Entries go into the current month's file in
  `00-system/learning/observations/` or
  `00-system/learning/organization-log/` (`YYYY-MM.md`); create it and add a
  table row if missing.
- **Patterns need evidence:** about three occurrences or owner confirmation.
- **A rule nothing checks does not hold.** When sessions that knew a rule
  keep breaking it, make a script or grep check it.

## Structural autonomy and its limits

Agents **may**, with a clear benefit and never for its own sake: move or
rename files, create or merge folders, split oversized files, consolidate
redundant AI-generated content, improve indexes, templates and workflows,
simplify metadata, fix links. No preemptive folders, no empty categories.
For significant changes: update every reference (`rg` the old path), log it
in the current month's organization-log file, update
[architecture.md](00-system/architecture.md) if the described state
changed, verify nothing was lost
([reorganization](00-system/workflows/reorganization.md)).

Agents **must not**, without explicit owner consent: delete important
historical information, irreversibly delete raw notes, send confidential
content to external systems, modify external systems, store secrets, or
perform mass destructive cleanup.

**Archive before delete** applies to canonical content. **Processed inbox
captures are the exception:** once triage has filed them, delete them. Git
history is the archive for raw captures.

**Priorities, in order:** reliable retrieval, fast context understanding,
few duplicates, low maintenance, low capture friction, small AI contexts,
machine readability, human readability, simple structure. Never pretty
trees, tag volume or ontological perfection.

## Git

Git is history, sync and the safety net that makes structural autonomy
acceptable.

- **Small, text-based changes,** no generated binaries. Inbox captures are
  atomic files so they merge without conflicts.
- **Before larger reorganizations** read `git status`, never destroy
  uncommitted changes you did not make, one logical change per commit.
- **Commit messages say what and why.** Run the
  [pre-commit checks](#pre-commit-checks) first: a push publishes, so the
  commit is the last gate.
- **Push without asking** once the checks passed, unless the owner says
  otherwise for a piece of work. Never rewrite pushed history.
- **Where work lands depends on the [operating mode](#operating-mode).**
  Single-session: `main`. Multi-session: the session branch, a pull request
  when the first draft stands, routine captures merged right away
  ([pull requests rule](.claude/rules/pull-requests.md)). Specs and plans
  are never committed, in either mode (same rule).

## Pre-commit checks

```bash
# 1. Links, anchors, frontmatter, code fences, max_lines, due evaluations
python3 00-system/scripts/linkcheck.py --orphans
# 2. Deletions: an additive change prints nothing. Not "^-[^-]": that
#    hides deleted bullet lines ("-- item").
git diff --cached | grep "^-" | grep -v "^--- "
# 3. Style: one pattern per owner rule. Keep LC_ALL: under POSIX, grep -P
#    compares bytes and multi-byte characters give false hits.
LC_ALL=C.UTF-8 git diff --cached | grep "^+" | LC_ALL=C.UTF-8 grep -P "<pattern>"
# 4. Secrets: read every hit
git diff --cached | grep "^+" | grep -inE "password|passwd|api[_-]?key|secret|token|private key"
```

A style hit is text to rewrite or a documented exception (a verbatim quote,
a delimiter in a documented line format). Check 4 includes a look for
`confidential` content in a file not marked for it. A
[canary](00-system/scripts/canary.md) proves check 1 still finds problems.

## Privacy and security

- **Never store secrets.** Record where a secret lives, never its value.
- **Sensitivity:** `public`, `private` (default), `confidential`,
  `restricted`. Mark the non-default ones in frontmatter.
- **Never send repository content to external services** beyond what the
  current task requires. A standing exception is a decision, scoped to one
  service.
- **Third parties:** only what connects to the owner's life, projects or
  open loops. No profile building.
- Details: [privacy rule](.claude/rules/privacy-security.md). Fuller
  recording (medical, legal) is opt-in:
  [optional policies](00-system/optional-policies.md).

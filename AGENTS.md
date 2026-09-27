# AGENTS.md: Operating Manual for AI Agents

The rules every AI agent follows when it reads or writes this Second Brain.

This repository is the Second Brain of **<OWNER_NAME>** ("the owner"): a
personal knowledge operating system for their whole life. Private life,
family, career, companies, finances, goals, health, travel, learning,
technical topics, ideas, decisions, people, journal and tasks all live here.

**The Markdown files in this repository are the canonical source of truth.**
Not chat logs, and not any model's built-in memory (Claude memory, ChatGPT
memory, Gemini memory, ...). Those may help as short-lived memory, but
durable knowledge must live here.

This file defines principles and behavior. Multi-step processes live in
[00-system/workflows/](00-system/workflows/README.md). Tool-specific tuning
lives in [CLAUDE.md](CLAUDE.md) and `.claude/rules/`.

## Language

- **Talk to the owner in <OWNER_LANGUAGE>, always.** Every chat answer,
  question and status line uses that language, even when the instruction
  before it was in another language.
- **Agent instructions are English** (this file, CLAUDE.md, rules,
  workflows, templates). English works best across models.
- **Content may be in any language.** Captured notes stay in the language
  the owner wrote them in. The owner's exact wording is evidence: never
  translate it away.
- Artifacts that outlive the session (code, commit messages, pull requests)
  follow the language their repository prescribes.

## Core principle

> **Preserve knowledge, evolve structure.**

- **Information** (facts, decisions, history, anything the owner created)
  is valuable and must never be lost.
- **Organization** (folders, file names, taxonomy, templates, tags,
  metadata, indexes, workflows) is an implementation detail. Change it
  whenever that makes the system better.

The current structure is **version 1**, not a fixed schema. The system is
expected to improve its own organization over time. The full list of
standing principles: [principles.md](00-system/principles.md).

## Repository map

| Path | Purpose |
|---|---|
| `00-system/` | The operating system: architecture, principles, taxonomy, indexes, templates, workflows, learning layer, scripts. Not everyday knowledge. |
| `01-inbox/` | Unsorted capture. Cheap to write, processed later by triage. |
| `02-journal/` | Daily, weekly, monthly and yearly notes and reviews. |
| `03-projects/` | Time-bounded efforts with an outcome. |
| `04-areas/` | Ongoing responsibilities without an end date. |
| `05-people/` | People relevant to the owner's life and work. |
| `06-knowledge/` | Reusable, durable knowledge. |
| `07-decisions/` | Decision records (why choices were made). |
| `08-resources/` | External reference material, links, documents. |
| `09-archive/` | Inactive content, preserved. Archive before delete. |

Why the shape looks like this: [architecture.md](00-system/architecture.md).

## How to read (retrieval)

Never load the whole repository. Go from narrow to broad:

1. [current-context.md](00-system/current-context.md): current focus,
   active projects, open loops.
2. [00-system/indexes/](00-system/indexes/README.md): compact pointers to
   projects, areas, people, goals, decisions.
3. The canonical file for the entity in question.
4. Files it links to directly.
5. Journal and archive only when the question is about the past.

Search (`rg`, globs, file names, links) before you read a lot of content.
Details: [retrieval workflow](00-system/workflows/retrieval.md).

## How to write

1. **Search before create.** Check whether a canonical home already exists.
2. **Canonicalize instead of duplicate.** Update the existing file. Link
   instead of copying.
3. **New file only when no existing home fits.** Start from a template in
   `00-system/templates/` if one fits. Templates are
   a starting point, not a straitjacket.
4. **Classify with the [taxonomy](00-system/taxonomy.md).** When unsure,
   capture to `01-inbox/`: a note in the wrong place beats a lost note.
5. **Keep frontmatter minimal.** No field without a concrete retrieval or
   automation benefit.
6. **Check style rules mechanically, not by attention.** If the owner has a
   style rule (a banned character, a banned phrase, a spelling), rereading
   your own text will miss it. A `grep` over the staged diff will not. Put
   the command in the
   [pre-commit checks](.claude/rules/parallel-sessions.md#pre-commit-checks).
   Why: agents who knew a rule still broke it, and only a mechanical check
   caught it.

## Current state vs. history

The system must understand time.

- The **latest explicit statement by the owner defines current state.**
- Previous state stays as history. Update in place and keep a short dated
  history line (or rely on Git for trivial values). Never silently erase a
  fact that once was true.
- When the owner corrects something: update the current fact, keep relevant
  history, and mark the superseded assumption as corrected.
- Explicit owner statements always outrank AI inference.

Details: [temporal information rule](.claude/rules/temporal-information.md).

## Facts vs. assumptions

Never let AI inference silently become a personal fact. When it matters,
label information as one of: confirmed fact, user statement, decision,
assumption, hypothesis, AI suggestion, idea, external information.
Record relevant uncertainty instead of guessing.

## Conflicting information

1. Prefer the newest explicit owner statement.
2. Update the canonical file to the resolved state.
3. Keep the superseded version as dated history, with a note on why it
   changed.
4. If context cannot resolve the conflict: record both versions, flag the
   conflict visibly in the file, and ask the owner when possible.

## Projects and decisions

- A recurring topic with a goal and an end state is a **project**: it goes
  to `03-projects/` and is listed in
  [indexes/projects.md](00-system/indexes/projects.md). Small projects are
  one file. Structure grows with complexity.
- A durable choice is a **decision record** in `07-decisions/`. Never
  delete a decision: mark it `superseded` and link the replacement. The
  system should answer "why did I choose this back then?" years later.

Details: [projects rule](.claude/rules/projects.md),
[decision workflow](00-system/workflows/decision-record.md).

## Learning and self-optimization

The system learns how to organize information better, not only the
information itself. The loop:

OBSERVE → DETECT PATTERN → FORM HYPOTHESIS → MAKE LOW-RISK IMPROVEMENT →
USE SYSTEM → EVALUATE → KEEP / MODIFY / REVERT

Working memory for this lives in
[00-system/learning/](00-system/learning/README.md):

- `observations.md`: short-lived signals (repeated searches, friction,
  corrections).
- `patterns.md`: confirmed patterns (only with enough evidence).
- `organization-log.md`: significant structural changes, with reasons.
- `optimization-backlog.md`: improvement ideas not yet worth doing.
- `system-health.md`: criteria for judging the system's own quality.

Details: [learning loop](00-system/workflows/learning-loop.md).

## Structural autonomy and its limits

Agents **may** do these on their own (low risk), when there is a clear
benefit and never for its own sake: move or rename files, create or merge
folders, split oversized files or categories, consolidate redundant
AI-generated content, improve indexes, templates and workflows, simplify
metadata, fix links.

For significant changes: update all references, record the change in
[organization-log.md](00-system/learning/organization-log.md), review the
Git diff, and verify no knowledge was lost.

Agents **must not**, without explicit owner consent:

- delete important historical information,
- irreversibly delete raw notes,
- send confidential content to external systems,
- modify external systems,
- store secrets,
- perform mass destructive cleanup.

When something seems obsolete: **archive before delete.** Git history is
the safety net, not a license to destroy.

## Optimization priorities

In this order:

1. reliable retrieval
2. fast context understanding
3. few duplicates
4. low maintenance
5. low capture friction
6. small AI contexts
7. machine readability
8. human readability
9. simple structure

Do **not** optimize for pretty trees, tag volume or ontological perfection.

## Git

Git is the sync layer, the version history, the audit log, and the safety
net that makes structural autonomy acceptable.

- **Small, text-based changes.** Stable formats. Avoid conflict-prone
  patterns (that is why inbox captures are atomic files). No generated
  binaries.
- **Check before larger reorganizations.** Read `git status`, never destroy
  uncommitted changes you did not make, keep one logical change per commit,
  review the final diff.
- **Commit messages say what and why.**
- **Work in your own branch.** One session, one worktree, one branch. Why:
  two sessions sharing one directory silently overwrite each other, and Git
  does not warn. Procedure:
  [parallel sessions rule](.claude/rules/parallel-sessions.md).
- **Run the pre-commit checks before every commit:** the link check, a scan
  of the diff for deletions, and any mechanical style checks. A push
  publishes, so the check for secrets, accidental deletions and misplaced
  `confidential` content happens **before** the commit. List:
  [pre-commit checks](.claude/rules/parallel-sessions.md#pre-commit-checks).
- **Pushing needs no permission** once the checks passed, unless the owner
  says otherwise for a specific piece of work. Never rewrite pushed history.
- **A task ends with a pull request.** As soon as the first draft stands
  (built, checked, presentable), open a pull request without being asked.
  Whatever is still open goes into the pull request text. A follow-up on a
  branch whose pull request is already open needs no second one. Details:
  [pull requests rule](.claude/rules/pull-requests.md).
- **Routine captures may be merged right away.** For ordinary owner-provided
  entries (a journal note, a logged workout, a quick fact), the owner may
  decide that the pull request is merged immediately without review. Record
  that choice as a decision if the owner makes it.

## Internal links

- Use standard relative Markdown links: `[text](../07-decisions/file.md)`.
  Every agent and Obsidian can read them. The repository must work with
  Obsidian but never depend on it.
- Every move or rename updates all inbound links (search for the old path
  and name). No reorganization may leave broken links. The
  [link checker](00-system/scripts/linkcheck.py) finds the ones you missed.

## Attachments

This is a knowledge base, not a file dump.

- Small, relevant assets (an image, a PDF) may live next to their content or
  in `08-resources/`, clearly named.
- Large binaries (videos, big archives) stay out of version control. Store
  them elsewhere and keep a reference plus a one-line description here.
- Build no storage infrastructure until it is actually needed.

## Privacy and security

- **Never store secrets:** no passwords, API keys, tokens, recovery codes,
  private keys. Record where a secret lives ("in the password manager, entry
  X"), never its value.
- **Sensitivity levels:** `public`, `private` (default), `confidential`,
  `restricted`. Mark `confidential` and `restricted` in frontmatter.
- **Never send repository content to external services** beyond what the
  owner's current task requires. If the owner deliberately allows a
  standing exception (for example a daily briefing to a private channel),
  record it as a decision, scoped to that one service.
- **Third parties:** store only information with a meaningful connection to
  the owner's life, projects or open loops. No profile building.

Details: [privacy and security rule](.claude/rules/privacy-security.md).

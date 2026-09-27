# Second Brain Blueprint

A ready-to-use blueprint for an **AI-native Second Brain**: your whole life's
knowledge as plain Markdown files in a Git repository, maintained by AI
agents that capture, file, review and even improve the system itself.

This is the structure I run my own Second Brain on every day. The private
original holds my real notes; this repository holds everything else: the
folder schema, the agent instructions, the workflows, the templates, the
checks and the lessons learned. Changes to my own system flow back here.

## Why this exists

Most note systems fail in one of two ways. Either capturing is so much work
that you stop doing it, or everything lands in one pile and you never find
it again. AI chat assistants add a third problem: their "memory" is locked
inside one vendor and quietly forgets or invents things.

This blueprint takes a different approach:

- **Markdown files in Git are the source of truth.** Not a chat history, not
  a vendor's memory. Every agent (Claude Code, Codex, Gemini, Cursor, ...)
  and every editor (Obsidian, VS Code, plain `cat`) can read them.
- **Capturing is cheap, organizing is the agent's job.** You drop a thought
  into the inbox; the agent files it in the right place later.
- **The system organizes itself and learns.** It notices friction, records
  patterns with evidence, makes small reversible improvements and checks
  later whether they worked.
- **Git is the safety net.** Every change is a commit, nothing is lost,
  every structural change can be reverted.

## How it works

```
  you ──capture──▶ 01-inbox/ ──triage──▶ projects, areas, people,
                                         knowledge, decisions, journal
                                                  │
         reviews (daily, weekly, monthly) ◀───────┘
                    │
                    ▼
  learning layer: observations ─▶ patterns ─▶ small improvement
                    ▲                               │
                    └──────── evaluation ◀──────────┘
```

1. **Capture:** tell the agent "note this" or drop a file into `01-inbox/`.
2. **Triage:** the agent searches for the existing home of each capture and
   files it there, instead of creating duplicates.
3. **Recall:** ask questions ("why did I choose X?", "what is open for Y?").
   The agent reads narrow to broad: current context, indexes, then the one
   canonical file.
4. **Review:** daily notes, weekly and monthly reviews condense what
   happened and check on projects and goals.
5. **Learn:** friction and corrections become observations, repeated ones
   become patterns, and patterns lead to small, logged, reversible changes
   that are evaluated at the next review.

Scheduled cloud routines can run the journal, the reviews and the inbox
triage for you every day. See
[00-system/workflows/automation.md](00-system/workflows/automation.md).

## What is inside

| Path | What it is |
|---|---|
| [`AGENTS.md`](AGENTS.md) | The operating manual every AI agent reads first |
| [`CLAUDE.md`](CLAUDE.md) | Extra rules for Claude Code |
| [`.claude/rules/`](.claude/rules/) | Short, focused behavior rules |
| [`.claude/skills/`](.claude/skills/) | Claude Code skills: capture, triage, recall, review, decision, project, system |
| [`00-system/`](00-system/README.md) | The operating system: principles, taxonomy, indexes, templates, workflows, learning layer, checks |
| `01-inbox/` to `09-archive/` | Where your knowledge lives, one folder per kind |

The folders in detail:

| Folder | Holds |
|---|---|
| `01-inbox/` | Unsorted captures, processed later |
| `02-journal/` | Daily, weekly, monthly and yearly notes |
| `03-projects/` | Efforts with a goal and an end |
| `04-areas/` | Ongoing responsibilities (health, finances, family, work, ...) |
| `05-people/` | People who matter in your life and work |
| `06-knowledge/` | Reusable knowledge you want to keep |
| `07-decisions/` | Decision records: what you chose and why |
| `08-resources/` | External references and documents |
| `09-archive/` | Inactive content, kept, never deleted |

## Quick start

1. Click **Use this template** on GitHub (or clone and push to your own
   private repository). Keep your copy **private**: it will hold your life.
2. Open it with an AI coding agent, for example
   [Claude Code](https://claude.com/claude-code).
3. Say: *"Set up my Second Brain."* The agent follows
   [GETTING-STARTED.md](GETTING-STARTED.md) and asks for your name,
   language and time zone.
4. Start capturing: *"Note that I want to renew my passport before May."*
5. Once a week, say *"weekly review"*. Or set up the scheduled routines and
   let it run by itself.

Step by step, including the automation: [GETTING-STARTED.md](GETTING-STARTED.md).

## Design principles

- **Preserve knowledge, evolve structure.** Facts, decisions and history are
  never lost. Folders, names, templates and workflows may change whenever
  that makes the system better.
- **Search before create.** One fact, one canonical place. Link, do not copy.
- **Current state vs. history.** The newest statement by the owner wins; the
  old value stays as dated history.
- **Facts vs. assumptions.** AI inference never silently becomes a fact.
- **A rule that no mechanism checks does not hold.** Important rules come
  with a script: [`linkcheck.py`](00-system/scripts/linkcheck.py) checks
  links, anchors, orphans, frontmatter and overdue evaluations, and it
  carries a canary so it cannot silently report green.
- **Small, reversible steps.** Evolution over revolution. Every significant
  change is logged with a date to evaluate it.

The lessons behind these principles, each learned the hard way in daily
use, are collected in
[00-system/learning/patterns.md](00-system/learning/patterns.md).

## FAQ

**Do I need Claude Code?** No. The instructions live in `AGENTS.md` and
work with any agent that reads repository instructions. Claude Code gets the
most out of it because of the skills and scheduled routines.

**Do I need Obsidian?** No. Links are standard relative Markdown links.
Obsidian works nicely on top, but the system never depends on it.

**What about privacy?** Your copy should be a private repository. The rules
forbid storing secrets (passwords, tokens) and support sensitivity levels
(`confidential`, `restricted`) in frontmatter. Anything you send to an AI
provider leaves your machine; decide consciously what goes in.

**Can I change the structure?** Yes, that is the point. The structure is
version 1, not a fixed schema. The agent may reorganize, as long as no
knowledge is lost and the change is logged.

## Staying up to date

This blueprint follows my own Second Brain. When I improve a workflow, a
rule or a check there, the generalized version lands here. Watch the
repository or compare your copy with new releases from time to time; the
[organization log](00-system/learning/organization-log.md) explains why
things changed.

## About the author

I am **Tim Rutte**, a cloud and software architect for business-critical
systems with more than 20 years of backend experience. I build systems that
run reliably, and lately more and more of them put AI to productive use.
This blueprint is what I use to run my own life and work.

More about me and my work: [timrutte.de](https://timrutte.de)

## License

[MIT](LICENSE). Use it, adapt it, build your own.

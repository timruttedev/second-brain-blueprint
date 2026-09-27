---
type: system
status: active
---

# Vision: from knowledge store to personal AI operating system

Where this repository is meant to go. Target state, not current state.

It complements [architecture.md](./architecture.md) (how it is built today)
and [principles.md](./principles.md) (what always holds). Concrete ideas
from here that are not yet worth doing live in the
[optimization backlog](./learning/optimization-backlog.md).

## The core: a context machine for AI

The Second Brain is, at its core, a **context machine for AI**.

The goal is not a big folder of Markdown. It is a system that knows the
owner so well (wishes, knowledge, projects, decisions, habits, contacts,
history) that a few words are enough for an AI to produce the result they
want. It is meant to be fed for a lifetime.

## Three layers

### Layer 1: sensors and input channels

Everything that brings context into the system:

- direct capture (typed or dictated notes, conversations with an AI),
- optional ingest pipelines (selected mail, scanned documents, voice notes,
  activity data) that drop atomic captures into `01-inbox/`,
- changes in the owner's other repositories and tools.

Not every mail or document should be stored. The goal is a high share of
signal, not a second archive next to the original sources.

### Layer 2: long-term context and memory

Essentially today's structure: facts, people, projects, decisions with
reasons, goals, history, habits, preferences, recurring patterns.

### Layer 3: proactive intelligence

The layer that asks instead of waiting to be asked:

- **Context-aware challenges** derived from the owner's own goals, with
  prioritization across life areas rather than rigid habit tracking.
- **Procrastination signals:** a task mentioned repeatedly but never
  started, a priority project without activity. Delivered as a concrete
  hint with the smallest next step, not as a report.
- **Baseline monitoring:** noticing a drop in activity or energy compared
  to the owner's own normal. Pattern recognition, never a diagnosis.
- **Positive patterns:** which routines correlate with good days and strong
  progress.
- **Board of advisors:** several AI roles look at an important decision
  separately (business, career, technology, finances, long-term goals) with
  the same long-term context, then merge their views.
- **A conversational interface** (a chat bot) that writes on its own when a
  pattern justifies it and writes learnings back into the repository.

## Design principles for this vision

- **Ingestion first.** A reliable data base comes before aggressive
  proactivity. A proactive coach is only as good as its context.
- **Signal over noise.** Extract what is relevant and make it canonical.
  Do not store everything unfiltered.
- **Keep history.** Without comparability over time, pattern recognition
  and learning are worthless
  ([temporal information](../.claude/rules/temporal-information.md)).
- **Separate fact and interpretation.** A detected pattern is a hypothesis,
  not a truth ([knowledge integrity](../.claude/rules/knowledge-integrity.md)).
- **Personal baseline, not norms.** Compare the owner with their own normal
  state, not with averages.
- **Proactive, not annoying.** Hints must be relevant, prioritized and
  actionable. A bot with trivial warnings gets ignored.
- **Privacy grows in importance** as more life areas flow together: access
  control, data minimization and deliberate rules for external services
  ([privacy and security](../.claude/rules/privacy-security.md)).
- **Automation with a learning loop.** Automated input should lead to
  better future decisions, not just more archive.

## Roadmap (example)

Order follows "ingestion first". Adjust it to the owner's priorities.

1. **Complete ingestion:** decide which channels matter, connect them one
   at a time, and check the signal quality of each.
2. **Scheduled upkeep:** daily journal, reviews and nightly triage run on
   their own ([automation](./workflows/automation.md)).
3. **Proactivity:** derive challenges and priorities from the repository.
4. **Interaction:** a conversational interface that reads and writes the
   repository.

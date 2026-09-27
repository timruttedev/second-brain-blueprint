# 00-system

The operating system of the Second Brain: how it works and how it improves
itself. Not everyday knowledge.

| File / dir | Role |
|---|---|
| [architecture.md](./architecture.md) | Current architecture and why. What is stable and what may evolve. Always describes the present state. |
| [current-context.md](./current-context.md) | Compact AI entry point: current focus, active projects, goals, open loops. Deliberately small. |
| [optional-policies.md](./optional-policies.md) | Policies that are off by default (for example recording medical or legal documents in full), with how to activate them. |
| [principles.md](./principles.md) | Standing principles. Change rarely, and only deliberately. |
| [taxonomy.md](./taxonomy.md) | Information types and the minimal metadata schema. Evolvable, changes are logged. |
| [vision.md](./vision.md) | Where the system is meant to go. Target state, not current state. |
| [indexes/](./indexes/README.md) | Compact pointers (projects, areas, people, goals, decisions, todos). Signposts, never copies of content. |
| `templates/` | Starting points for new files. Adaptive, not mandatory. |
| [workflows/](./workflows/README.md) | Model-agnostic process docs: capture, triage, retrieval, reviews, learning loop, reorganization, automation. |
| [learning/](./learning/README.md) | The self-learning layer: observations, patterns, organization log, optimization backlog, system health. |
| `scripts/` | Python for the few jobs a hand-typed one-liner gets wrong: the link checker ([linkcheck.py](./scripts/linkcheck.py)) with its [canary](./scripts/canary.md), and a report of unmerged branches ([branch_overview.py](./scripts/branch_overview.py)). Logic only: knowledge stays in Markdown. |

Rule of thumb: a change here that alters how agents behave gets a commit of
its own with a clear message and, when structural, an entry in the current month's file in
[organization-log/](./learning/organization-log.md).

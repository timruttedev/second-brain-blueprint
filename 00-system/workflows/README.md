# Workflows

Model-agnostic process documentation: **these files are the canonical
definition of every workflow.** Agent-specific implementations (for example
the Claude Code skills in `.claude/skills/`) are conveniences on top. If a
skill and a workflow doc diverge, the workflow doc wins and the skill gets
fixed.

| Workflow | File | Claude skill |
|---|---|---|
| Capture | [capture.md](./capture.md) | `/brain-capture` |
| Inbox triage | [triage.md](./triage.md) | `/brain-triage` |
| Recall / retrieval | [retrieval.md](./retrieval.md) | `/brain-recall` |
| Create project | [create-project.md](./create-project.md) | `/brain-project` |
| Decision record | [decision-record.md](./decision-record.md) | `/brain-decision` |
| Daily / weekly / monthly / yearly review | [reviews.md](./reviews.md) | `/brain-review` |
| Learn (the learning loop) | [learning-loop.md](./learning-loop.md) | `/brain-system learn` |
| Organize (safe reorganization) | [reorganization.md](./reorganization.md) | `/brain-system change` |
| Optimize (whole-system review) | [optimize.md](./optimize.md) | `/brain-system judge` |
| Archive | [archive.md](./archive.md) | (part of triage and organize) |
| System health check | [system-health-check.md](./system-health-check.md) | `/brain-system check` |
| Scheduled cloud routines | [automation.md](./automation.md) | (no skill, set up once in the routines UI) |

Related, but not workflows: principles ([principles.md](../principles.md)),
taxonomy and metadata ([taxonomy.md](../taxonomy.md)), autonomy limits
([AGENTS.md](../../AGENTS.md)).

## Adding your own workflow

A workflow earns a file here when a multi-step process repeats and an agent
would otherwise reinvent it each time. Add a row to the table above, link it
from the skill that runs it (if any), and keep it short: steps, checks, and
one "Why:" line where a step is not obvious.

---
paths:
  - "03-projects/**"
  - "04-areas/**"
---

# Rule: Projects and Areas

How projects and areas are created, updated and closed.

- **Project or area?** A project has a definable end state. An area is an
  ongoing responsibility. A recurring theme without an end is an area, not
  a stale project.
- **New project:** start from the project template
  (`00-system/templates/project.md`) as ONE file, add it to
  [indexes/projects.md](../../00-system/indexes/projects.md), and link its
  owning area. Turn it into a folder only when the file actually grows
  (the main file becomes `README.md`). Workflow:
  [create project](../../00-system/workflows/create-project.md).
- **Every meaningful update touches** the project's "Current state" and
  "Next steps", its `updated:` date, and (if focus changed)
  [current-context.md](../../00-system/current-context.md).
- **Durable project decisions go to `07-decisions/`** and are linked from
  the project's "Key decisions", not buried in the log.
- **Finished or dead projects:** set the status, move to
  `09-archive/projects/`, remove from the index, fix links
  ([archive workflow](../../00-system/workflows/archive.md)). Detect
  stagnation (months without movement) during reviews and say so.
- **Areas emerge from usage.** Create one when triage repeatedly routes
  captures to the same life domain, not speculatively.

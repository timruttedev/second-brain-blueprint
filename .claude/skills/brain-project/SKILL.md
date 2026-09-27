---
name: brain-project
description: Create or update a project in the Second Brain, meaning new endeavors with a definable outcome, status updates, next steps and blockers. Use when the user starts something new ("new project", "I'm going to build...", or the same in their own language) or reports project progress.
---

# Brain Project

Projects are time-bounded efforts with a definable end state. Canonical
workflow: [create-project.md](../../../00-system/workflows/create-project.md).
Template: [project.md](../../../00-system/templates/project.md). The
workflow doc wins on any conflict with this file.

**New project:**

1. Check that it is a project: can "done" be defined? If it is ongoing, it
   is an area (`04-areas/`).
2. Search for an existing or archived project first (`03-projects/`,
   `09-archive/`).
3. Create ONE file: `03-projects/<name>.md`.
4. Register it in `00-system/indexes/projects.md`, link it from its area,
   and add it to `00-system/current-context.md` if it is current focus.

**Update:** edit current state, next steps, blockers and log in the project
file, touch `updated:`, record durable decisions via the decision workflow,
and update the index and current context when status or focus changed.

Turn the file into a folder only when it actually outgrows one file, and
fix all links when you do.

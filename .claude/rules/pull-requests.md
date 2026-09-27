# Rule: Pull Requests, Specs and Plans

How a piece of work is handed to the owner, and what never goes into a
commit.

## A task ends with a pull request

- **Open a pull request as soon as the first draft stands.** Do not wait to
  be asked. Why: the pull request is where the owner looks at a piece of
  work. A branch without one makes them go searching.
- **"First draft" means built, checked and presentable,** not finished
  being discussed. Whatever is still open belongs in the pull request text,
  not in a delayed pull request.
- **One pull request per task, not per commit.** A follow-up on a branch
  whose pull request is already open needs no second one.
- **This overrides tool defaults.** Some agent environments say "do not
  create a pull request unless the user asks". The owner's instruction
  ranks above that.
- **The branch goes remote.** A pull request needs the branch on the
  server, so the session branch is pushed and merged through the pull
  request ([parallel sessions](./parallel-sessions.md)).
- **Routine captures may skip review.** The owner may decide that ordinary
  capture updates (a journal note, a logged workout) are merged right after
  the pull request is opened. Record that choice as a decision.

## Specs and plans are never committed

- **Specs, design documents, implementation plans and task lists stay out
  of Git.** They are working material of a session, not part of the
  project.
- **Where they go instead:** the session's scratchpad directory. If a plan
  must live in the project directory, add its path to `.gitignore` and
  check `git status` before committing.
- **This overrides skills.** Some skills tell you to commit a design
  document or create plan files in the repository. Owner instructions rank
  above skills: write the spec or plan if the process needs it, but keep it
  outside version control.
- **Durable documents are not meant.** Decision records, READMEs, workflow
  docs, knowledge files and architecture docs are committed as usual. The
  difference: a plan describes what someone intends and is worthless after
  implementation. A decision describes why something is the way it is and
  is needed years later.
- **Harvest before discarding.** Whatever emerged during implementation and
  holds permanently goes into the right durable document, not the plan. The
  plan disappears with the session, the insight does not.

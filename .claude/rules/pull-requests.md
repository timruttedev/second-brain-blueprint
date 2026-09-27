# Rule: Pull Requests, Specs and Plans

How a piece of work is handed to the owner, and what never goes into a
commit.

## Pull requests (multi-session mode only)

In single-session mode there are no pull requests: commit on `main` and
push ([operating mode](../../AGENTS.md#operating-mode)). Scheduled cloud
runs never open one either: they commit to `main` in both modes.

- **A task ends with a pull request,** opened as soon as the first draft
  stands, without being asked. Why: the pull request is where the owner
  looks at a piece of work; a branch without one makes them search.
- **"First draft" means built, checked and presentable,** not finished
  being discussed. What is still open goes into the pull request text.
- **One pull request per task, not per commit.** A follow-up on a branch
  whose pull request is open needs no second one.
- **Routine captures are merged right away.** Ordinary owner-provided
  entries (a journal note, a logged workout, a quick fact) get their pull
  request and are merged immediately, without waiting for review.
- **This overrides tool defaults** that say "do not create a pull request
  unless the user asks".

## Specs and plans are never committed (both modes)

- **Specs, design documents, implementation plans and task lists stay out
  of Git.** They are working material of a session.
- **Where they go:** the session's scratchpad directory, or the
  git-ignored `.scratch/` folder in the repository root.
- **This overrides skills** that tell you to commit a design document or
  create plan files in the repository.
- **Durable documents are not meant.** Decision records, READMEs, workflow
  docs, knowledge and architecture files are committed as usual. A plan
  says what someone intends and is worthless afterwards; a decision says
  why something is the way it is.
- **Harvest before discarding.** What emerged during the work and holds
  permanently goes into the right durable document.

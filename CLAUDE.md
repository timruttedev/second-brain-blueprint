# CLAUDE.md

Claude Code specifics on top of the model-agnostic operating manual.

@AGENTS.md

## Claude Code specifics

[AGENTS.md](AGENTS.md) is canonical for all agents. The rules below only
tune Claude Code's behavior. They add nothing another agent would need.

### Start of session: work in a worktree

**Before writing anything, put the session in its own worktree on its own
branch:** `git fetch`, `git merge origin/main`, then
`EnterWorktree(name: "<topic>")`. Never edit the main checkout directly,
unless the owner explicitly says otherwise.

Why: two sessions sharing one directory silently overwrite each other, and
Git does not warn. Procedure and merge-back steps:
[parallel sessions rule](.claude/rules/parallel-sessions.md).

### Context discipline

- Keep context small. Never read the whole repository. Follow the retrieval
  hierarchy in AGENTS.md: `current-context.md`, then indexes, then the
  canonical file.
- Prefer `Grep` and `Glob` over reading directories of files. Load journal
  and archive content only when the question is about the past.
- Detailed, path-scoped behavior lives in `.claude/rules/`.
  Rely on those instead of rereading workflow docs every session.

### Before writing

- Use existing knowledge before generating new content.
- Search before creating any file. Update canonical files instead of
  creating duplicates.
- Use the skills in `.claude/skills/` for capture, triage, recall, reviews,
  decisions, projects and system upkeep. The model-agnostic versions of
  these workflows live in
  [00-system/workflows/](00-system/workflows/README.md). If a skill and a
  workflow doc disagree, the workflow doc wins: fix the skill.

### End of session

- Before wrapping up a substantial session, check briefly: did this session
  produce durable knowledge, a correction, a decision, a confirmed pattern
  or a system improvement that is not yet in the repository? If yes,
  persist it (the `brain-system` skill, mode `learn`).
- Store distilled, future-useful knowledge only. This is not a chat
  archive.

### Learning from the owner

- Treat explicit corrections as signals. Fix the canonical file immediately
  and note repeated corrections in
  [observations.md](00-system/learning/observations.md).
- Recognize durable decisions and preferences in conversation. Offer to
  record decisions in `07-decisions/` and preferences in
  [patterns.md](00-system/learning/patterns.md) (with evidence), so they do
  not evaporate with the chat.
- Claude's own memory is auxiliary only, never the only place something
  important lives. Persist important knowledge in this repository.

### Instructions that override Claude Code defaults

- **Open a pull request when the first draft stands**, without being asked.
  This overrides the default "do not create a pull request unless asked".
  See [pull requests rule](.claude/rules/pull-requests.md).
- **Never commit specs or plans.** Keep them in the session scratchpad,
  even when a skill says to commit them. Owner instructions rank above
  skills.

### Safety

- Git history is the safety net. Prefer ordinary commits with clear
  messages over defensive copies of files.
- Archive before delete (`09-archive/`). Never rewrite published history.
- Follow the autonomy limits in AGENTS.md. When a change feels large or
  destructive, ask first.

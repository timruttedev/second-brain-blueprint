# CLAUDE.md

@AGENTS.md

## Claude Code specifics

[AGENTS.md](AGENTS.md) is canonical for all agents. The lines below only
tune Claude Code; they add nothing another agent would need.

### Start of session

- **Read the `Mode:` line** in AGENTS.md
  ([operating mode](AGENTS.md#operating-mode)).
- **single-session** (default): work in the main checkout on `main`.
  `git pull` first, so you see what scheduled runs pushed.
- **multi-session:** before the first write, `git fetch`, then
  `EnterWorktree(name: "<topic>")`, then `git merge origin/main` inside the
  worktree. Never edit or merge in the main checkout
  ([multi-session rule](.claude/rules/parallel-sessions.md)).
- **Scheduled cloud runs** work directly on `main` in both modes: their
  checkout is already their own.

### Context discipline

Follow the retrieval order in AGENTS.md; prefer `Grep` and `Glob` over
reading directories. Path-scoped rules in `.claude/rules/` load when you
touch those paths; rely on them instead of rereading workflow docs.

### Skills

Use the skills in `.claude/skills/` for capture, triage, recall, reviews,
decisions, projects and system upkeep. The model-agnostic versions live in
[00-system/workflows/](00-system/workflows/README.md). If a skill and a
workflow doc disagree, the workflow doc wins: fix the skill.

### End of session

Before wrapping up a substantial session, check: did it produce durable
knowledge, a correction, a decision, a confirmed pattern or a system
improvement that is not yet in the repository? If yes, persist it
(`brain-system` skill, mode `learn`). Distilled knowledge only, not a chat
archive. During the session, offer to record durable decisions in
`07-decisions/` and preferences in the patterns file, so they do not
evaporate with the chat. Claude's own memory is auxiliary, never the only
place something important lives.

### Overrides of Claude Code defaults

- **Multi-session mode only: open a pull request when the first draft
  stands,** without being asked. This overrides the default "do not create
  a pull request unless asked"
  ([pull requests rule](.claude/rules/pull-requests.md)). In single-session
  mode there is no pull request.
- **Never commit specs or plans,** even when a skill says so. Owner
  instructions rank above skills.
- **`.claude/settings.json`:** `worktree.baseRef: "head"` starts
  worktrees from local `HEAD`, keeping unpushed commits (multi-session).

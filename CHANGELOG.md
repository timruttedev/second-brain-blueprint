# Changelog

All notable changes to this blueprint are documented here. The format
follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the
project uses [Semantic Versioning](https://semver.org/). A change that
needs action in your own copy is marked **Upgrade note**.

## [Unreleased]

### Added

- `00-system/scripts/init.py`: sets up a copy in one command (name,
  language, time zone), removes blueprint-only material and replaces the
  README with an owner version. Supports `--dry-run` and `--keep-examples`.
- `examples/`: a small, complete, fictional Second Brain, including a
  capture before and after triage.
- Operating modes: single-session mode (default, commits to `main`) and
  opt-in multi-session mode (worktree per session, pull request per task),
  switched in `AGENTS.md`.
- `00-system/optional-policies.md`: opt-in policies, such as recording
  medical documents or legal matters in full.
- CI workflow that runs the link checker and the script tests on every push
  and pull request.
- README: CI and license badges, a diagram of the flow, a glossary, more
  FAQ answers and an upgrade guide.
- GETTING-STARTED: requirements, an agent checklist for the first setup,
  and a short explanation of the operating modes.
- CONTRIBUTING, SECURITY, issue templates and a pull request template.

### Changed

- **Upgrade note:** the learning logs keep their entries in month files
  (`00-system/learning/observations/YYYY-MM.md`,
  `00-system/learning/organization-log/YYYY-MM.md`); the files of the same
  name one level up are signposts with the format and a month table. Move
  existing entries into month files.
- Processed captures are deleted after triage; Git history is the archive
  for raw captures.
- The unattended daily journal run covers the seven days before today,
  writes no file for a day without evidence, and only appends to an
  existing daily. Unattended weekly reviews leave the inbox to the nightly
  triage.
- The quarterly look outside runs in the monthly reviews written in
  January, April, July and October.
- Recording medical documents and legal matters in full is no longer a
  default, but an opt-in policy.

### Removed

- The link checker's legacy alias for `--orphans`. **Upgrade note:** use
  `--orphans` in scripts and routine prompts.

## [0.1.0] - 2026-09-27

### Added

- Initial release: folder schema `00-system/` to `09-archive/`, agent
  instructions (`AGENTS.md`, `CLAUDE.md`, `.claude/rules/`), Claude Code
  skills, model-agnostic workflows, templates, indexes, the learning layer
  with seed patterns, the link checker with its canary and tests, and the
  guide for scheduled cloud routines.

[Unreleased]: https://github.com/timruttedev/second-brain-blueprint/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/timruttedev/second-brain-blueprint/releases/tag/v0.1.0

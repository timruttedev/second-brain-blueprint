# Getting started

How to turn this blueprint into your own Second Brain. You can do every step
yourself, or open the repository with an AI agent and say *"Set up my
Second Brain"*: the agent follows this file.

## 1. Make your own private copy

- On GitHub: **Use this template** → **Create a new repository** →
  choose **Private**.
- Or: clone this repository, create an empty private repository of your
  own, and push to it.

Keep it private. It will hold your health, money, family and work.

## 2. Fill in the placeholders

Search the repository for these placeholders and replace them:

| Placeholder | Meaning | Example |
|---|---|---|
| `<OWNER_NAME>` | Your first name, so the agent knows who "the owner" is | `Alex` |
| `<OWNER_LANGUAGE>` | The language the agent talks to you in | `English`, `German` |
| `<TIMEZONE>` | Your time zone, used for journal dates | `Europe/Berlin` |

```bash
grep -rn "<OWNER_NAME>\|<OWNER_LANGUAGE>\|<TIMEZONE>" --include="*.md" .
```

Agent instructions stay in English (every model follows them best that way).
Your notes can be in any language.

## 3. Write your starting point

Two files give the agent its orientation. Fill them with a few lines each;
they grow by themselves later.

- [`00-system/current-context.md`](00-system/current-context.md): what you
  are focused on right now, active projects, open loops.
- [`00-system/indexes/`](00-system/indexes/README.md): the first entries for
  your projects, areas (for example health, finances, family, work) and the
  most important people.

Tip: just tell the agent about your life for ten minutes. *"I work as ...,
I'm currently renovating ..., my main goals this year are ..."*. Then say
*"triage"*. It files everything and fills the indexes.

## 4. Use it every day

| You say | What happens |
|---|---|
| *"Note that ..."* / *"capture ..."* | A capture lands in `01-inbox/` |
| *"triage"* | The inbox is sorted into its canonical homes |
| *"What do I know about ...?"* / *"Why did I ...?"* | The agent answers from the repository |
| *"I decided to ..."* | A decision record in `07-decisions/` |
| *"New project: ..."* | A project file in `03-projects/` |
| *"daily"*, *"weekly review"*, *"monthly review"* | Journal notes and reviews |
| *"Check the brain"* | Health check of the system itself |

With Claude Code these are skills in [`.claude/skills/`](.claude/skills/).
Other agents find the same processes in
[`00-system/workflows/`](00-system/workflows/README.md).

## 5. Check the system

Run the check before you commit, and whenever something feels off:

```bash
python3 00-system/scripts/linkcheck.py --orphans
```

It finds broken links and anchors, unknown frontmatter values, files over
their line budget and evaluations in the learning log that are overdue.
Exit code 0 means clean, 1 means findings, 2 means the check itself is
broken (its canary was not found).

The check scripts have their own tests:

```bash
python3 -m unittest discover -s 00-system/scripts -t 00-system/scripts
```

## 6. Optional: let it run by itself

Scheduled cloud agents can write the daily note, the weekly and monthly
reviews and triage the inbox every night, without you opening anything.
Setup, ready-to-paste prompts and the pitfalls:
[`00-system/workflows/automation.md`](00-system/workflows/automation.md).

Two things to know up front:

- Create the routine in the routines UI and **attach your repository**
  there. A routine without a repository runs, reports success and does
  nothing.
- Trust the **heartbeat commit**, not the routine's status. Every run writes
  [`00-system/sync/state/automation-runs.json`](00-system/sync/state/automation-runs.json);
  if that file stops changing, the automation is broken.

## 7. Let it evolve

Do not try to design the perfect structure up front. Use the system, and
let the learning loop do its job: friction becomes observations, repeated
observations become patterns, patterns become small changes that are
checked later. See
[`00-system/workflows/learning-loop.md`](00-system/workflows/learning-loop.md).

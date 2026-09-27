# Getting started

How to turn this blueprint into your own Second Brain, and how to use it
once it is set up.

<!-- blueprint-only:start -->
You can do every step yourself, or open the repository with an AI agent
and say *"Set up my Second Brain"*: the agent follows this file, in
particular the
[agent checklist](#agent-checklist-for-set-up-my-second-brain).
<!-- blueprint-only:end -->

> **Requirements**
>
> - **git**
> - **Python 3.10 or newer** (setup script and checks; standard library only)
> - **An AI coding agent** that reads repository instructions.
>   [Claude Code](https://claude.com/claude-code) is recommended: it also
>   uses the skills and can run the scheduled routines.
> - Optional: the GitHub CLI **`gh`** (pull requests, branch overview) and
>   **ripgrep `rg`** (faster search for the agent).

<!-- blueprint-only:start -->
Want to see where this leads first? [`examples/`](examples/README.md) is a
small, filled-in, fictional Second Brain.

## Make your own private copy

- On GitHub: **Use this template** → **Create a new repository** →
  choose **Private**.
- Or: clone this repository, create an empty private repository of your
  own, and push to it.

Keep it private. It will hold your health, money, family and work.

## Run the setup script

One command personalizes the copy:

```bash
python3 00-system/scripts/init.py --name "Alex" --language "English" --timezone "Europe/Berlin" --dry-run
python3 00-system/scripts/init.py --name "Alex" --language "English" --timezone "Europe/Berlin"
```

The first line only shows what would change; the second does it. The
script:

- fills in the placeholders `<OWNER_NAME>` (your first name, so the agent
  knows who "the owner" is), `<OWNER_LANGUAGE>` (the language the agent
  talks to you in) and `<TIMEZONE>` (used for journal dates);
- sets today's date in the current context and the indexes;
- removes blueprint-only parts: the `examples/` folder (keep it with
  `--keep-examples`), the changelog, the contribution and security docs,
  the issue templates, and sections like this one;
- replaces `README.md` with a short README for your own copy;
- runs the link checker and prints the next steps.

It is safe to run twice and refuses to run once no placeholders are left
(override with `--force`).

**Manual fallback,** if you cannot run Python: search for the placeholders
and replace them by hand, set the `updated:` dates in
`00-system/current-context.md` and `00-system/indexes/`, copy
`00-system/templates/README.owner.md` over `README.md`, and delete
`examples/` if you do not want it.

```bash
grep -rn "<OWNER_NAME>\|<OWNER_LANGUAGE>\|<TIMEZONE>" --include="*.md" .
```

Agent instructions stay in English (every model follows them best that way).
Your notes can be in any language.
<!-- blueprint-only:end -->

## Learn the one habit: capture

Everything starts with a capture: one thought, one small file in
`01-inbox/`, no decision about where it belongs. Say *"Note that the
dentist moved my appointment to Friday"* and the agent writes
`01-inbox/YYYY-MM-DD-HHMM-dentist-appointment.md`. Later, *"triage"* files
each piece in its canonical home (a project, an area, a person, the to-do
list) and deletes the capture; Git keeps the original.

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

## Write your starting point

Two places give the agent its orientation. A few lines each are enough;
they grow by themselves later.

- [`00-system/current-context.md`](00-system/current-context.md): what you
  are focused on right now, active projects, open loops.
- [`00-system/indexes/`](00-system/indexes/README.md): the first entries for
  your projects, areas (for example health, finances, family, work) and the
  most important people.

You do not have to write them yourself. Tell the agent about your life for
ten minutes, as captures: *"I work as ..., I'm currently renovating ...,
my main goals this year are ..."*. Then say *"triage"*. It files everything
and fills the indexes and the current context.

## Check the system

Run the check before you commit, and whenever something feels off:

```bash
python3 00-system/scripts/linkcheck.py --orphans
```

It finds broken links and anchors, orphaned files, unknown frontmatter
values, files over their line budget and evaluations in the learning log
that are overdue. Exit code 0 means clean, 1 means findings, 2 means the
check itself is broken (its canary was not found). The same check runs in
CI on every push.

The scripts have their own tests:

```bash
python3 -m unittest discover -s 00-system/scripts -t 00-system/scripts
```

## Pick an operating mode

- **Single-session mode (default):** one agent session at a time; it commits
  directly to `main` and pushes. Right for almost everyone.
- **Multi-session mode:** for several sessions in parallel. Each works in
  its own Git worktree and branch, and a task ends with a pull request.
  Switch by setting `Mode: multi-session` in the
  [operating mode section of AGENTS.md](AGENTS.md#operating-mode).

Scheduled cloud runs work directly on `main` in both modes: each has its
own isolated checkout.

## Optional: let it run by itself

Scheduled cloud agents can write the daily note, the weekly and monthly
reviews and triage the inbox every night, without you opening anything.
Setup, ready-to-paste prompts and the pitfalls:
[`00-system/workflows/automation.md`](00-system/workflows/automation.md).
Start with one routine, once the process has worked by hand.

Two things to know up front:

- Create the routine in the routines UI and **attach your repository**
  there. A routine without a repository runs, reports success and does
  nothing.
- Trust the **heartbeat commit**, not the routine's status. Every run writes
  [`00-system/sync/state/automation-runs.json`](00-system/sync/state/automation-runs.json);
  if that file stops changing, the automation is broken.

## Let it evolve

Do not try to design the perfect structure up front. Use the system, and
let the learning loop do its job: friction becomes observations, repeated
observations become patterns, patterns become small changes that are
checked on a fixed date. See
[`00-system/workflows/learning-loop.md`](00-system/workflows/learning-loop.md).

<!-- blueprint-only:start -->
## Agent checklist for "Set up my Second Brain"

For the agent. Work through it in order, in one session, and talk to the
owner in the language they choose in step 1.

1. **Ask** for three things: the owner's first name, the language to talk
   in, and their time zone (IANA name such as `Europe/Berlin`; suggest one
   from the system clock and let them confirm).
2. **Ask** whether to keep `examples/` for reference (default: no).
3. **Run** `python3 00-system/scripts/init.py --name NAME --language LANG --timezone TZ --dry-run`,
   show the summary, then run it without `--dry-run` (add
   `--keep-examples` if they said yes). If Python is unavailable, do the
   manual fallback above.
4. **Ask** about the starting point, one topic at a time, briefly:
   current focus and until when; active projects; areas of life they want
   to track (for example health, finances, family, work); the few people
   who matter for those; the top goals; anything with a deadline.
5. **Capture** the answers as files in `01-inbox/`, one per topic, in the
   owner's words.
6. **Triage** them following
   [`00-system/workflows/triage.md`](00-system/workflows/triage.md): create
   the project, area and person files from the templates, fill
   `00-system/current-context.md` and the indexes with one line and one
   link per entry, put deadlines into `00-system/indexes/todos.md`, and
   delete the processed captures.
7. **Check** with `python3 00-system/scripts/linkcheck.py --orphans` and fix
   every finding.
8. **Commit** with a message such as `Set up the Second Brain for NAME`
   and push (single-session mode commits to `main`).
9. **Tell** the owner the three things to say from now on: *"note that
   ..."*, *"triage"*, *"weekly review"*, and offer the scheduled routines
   from the section above once they have used the system for a week.
<!-- blueprint-only:end -->

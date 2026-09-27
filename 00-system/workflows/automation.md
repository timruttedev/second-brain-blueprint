# Workflow: Scheduled Cloud Routines

Purpose: let the Second Brain maintain itself while nobody is watching. Two
scheduled routines are enough: a **morning journal run** (daily notes plus
the weekly and monthly reviews) and a **nightly inbox triage**.

This page uses Claude Code routines (scheduled cloud agents, managed at
claude.ai/code/routines) as the example. Any scheduler that can start an
agent on a fresh checkout of this repository works the same way.

## The two routines

| Routine | Suggested schedule (UTC cron) | Follows | Heartbeat key |
|---|---|---|---|
| Journal and reviews | `0 7 * * *` (morning) | [reviews.md](./reviews.md) | `journal` |
| Inbox triage | `0 19 * * *` (evening) | [triage.md](./triage.md) | `triage` |

- **Twelve hours apart, on purpose.** Two routines writing to this
  repository at the same time race on the same files.
- **One journal routine, not three.** The weekly reads the dailies and the
  monthly reads the weeklies, so they run in order in one session.
- **Cron is UTC** and does not follow daylight saving time. Pick the hour
  for your `<TIMEZONE>` and accept a one-hour shift twice a year.

### What the journal run does

Each step is skipped when its output already exists:

| Step | Condition | Writes |
|---|---|---|
| Daily | any of the **last 7 days** has no file | `02-journal/daily/YYYY-MM-DD.md` |
| Weekly | the ISO week of *today minus 7 days* has no file | `02-journal/weekly/YYYY-Www.md` |
| Monthly | the **previous calendar month** has no file | `02-journal/monthly/YYYY-MM.md` |

The windows are the catch-up: a failed or skipped run is repaired by the
next one, without backfilling the whole history. Nothing is rewritten.

This routine is also the only carrier of the learning loop's feedback steps
(due evaluations in the weekly; health check, optimize, promotion and
thinning in the monthly). If it silently fails, the system stops learning.

## Setup

1. **Create each routine yourself in the routines UI and attach this
   repository there.** Why: a routine created by an agent (through an API
   or tool call) may start with no repository attached. It then runs on an
   empty workspace, does nothing, and still reports success.
2. Paste the matching prompt from below. Replace `<TIMEZONE>`.
3. Give the routine permission to push to `main`.
4. Start one manual test run and check for the heartbeat commit (next
   section). Only that commit proves the setup works.

## The heartbeat

Both routines end by writing themselves into
[`automation-runs.json`](../sync/state/automation-runs.json), under their
own key, and committing it **every time**, even when there was nothing else
to do:

```json
{
  "journal": {"last_run": "YYYY-MM-DDTHH:MM:SSZ", "status": "ok", "note": "one short line"},
  "triage":  {"last_run": "YYYY-MM-DDTHH:MM:SSZ", "status": "ok", "note": "one short line"}
}
```

- `last_run` is set to the current UTC time **on success only**. On failure
  it stays at the last successful value.
- `status` (`ok` or `failed`) and `note` are written either way.

Why a commit on a quiet day: without it, a failed run and an uneventful
night look identical from outside the repository.

Why `last_run` freezes on failure: a monitor usually reads only the
timestamp. If a failing run stamped it fresh, a routine that fails every day
would look healthy forever. With the freeze, a simple rule ("alert when
`last_run` is older than 36 hours") catches the second failure in a row. Do
not "fix" this by always updating `last_run`.

## Lessons

- **A routine's status says nothing about its effect.** "Succeeded" only
  means the agent session ended without an error. Only the heartbeat commit
  on `main` shows that the run had the repository and could push. The
  [health check](./system-health-check.md) verifies both.
- **Keep the prompt short and point to the workflow docs, which override
  it.** The prompt lives outside the repository, so it drifts silently when
  the docs change. A short prompt that says "the workflow doc wins, report
  any contradiction" drifts less and lets a run flag the gap itself.
- **Change the prompt first, then the docs.** Editing only this repository
  documents an intention; it does not change the run. If the prompt needs a
  new script, merge the script first, then update the prompt the same day.
- **Every path a prompt names must exist.** Let the run check them as step
  0 and report any missing one in its heartbeat note.
- **No worktree.** Each run gets its own cloud checkout, which already
  gives the isolation the [worktree rule](../../.claude/rules/parallel-sessions.md)
  asks for. The runs work directly on `main`, commit and push. This
  exception holds only while nobody else works in that checkout.
- **The checkout may be shallow and stale.** A local `main` can be days
  behind, and `refusing to merge unrelated histories` is then a
  shallow-clone artifact, not rewritten history. With a clean tree, the
  gentle fix is `git fetch origin main`, `git switch --detach origin/main`,
  and at the end `git push origin HEAD:main`. Avoid `reset --hard`.
- **Unattended means no guessing.** Nobody can answer a question at night,
  so an undecidable item stays where it is with a one-line note.
- **The cloud clones everything**, including `confidential` and
  `restricted` files. Running routines in the cloud is a conscious owner
  decision; record it in `07-decisions/`. A local scheduler avoids it.

## Example prompt: journal and reviews

```text
You are the scheduled journal run for this Second Brain repository. Nobody is watching: work autonomously, finish, push, ask nothing.

This is the only routine that writes the weekly and monthly reviews and with them the learning loop's feedback steps. If this run skips them, nobody does them.

RULES
1. Read AGENTS.md and CLAUDE.md first; they and .claude/rules/ are binding. The repository wins over this prompt; report any contradiction.
2. No worktree. Work on main, commit, push (exception in 00-system/workflows/automation.md).
3. Follow 00-system/workflows/reviews.md. It overrides this prompt if the two disagree.
4. Journal files are immutable: an existing file means that period is done.
5. Step 0: check that every path named here exists. Name any missing one in the heartbeat note and in 00-system/learning/observations.md.

CHECKOUT
The checkout may be shallow and local main may be stale. "refusing to merge unrelated histories" is a shallow-clone artifact. With a clean tree: git fetch origin main, git switch --detach origin/main, and at the end git push origin HEAD:main.

DATES
Journal days are <TIMEZONE> days. Compute dates with TZ=<TIMEZONE> date. For day boundaries use: TZ=<TIMEZONE> git log --no-merges --date=format-local:'%Y-%m-%d %H:%M' --format='%ad %h %s'
Never write a journal file for a period without evidence, and nothing before the first commit.

STEP 1, DAILY: for each of the last 7 days without 02-journal/daily/YYYY-MM-DD.md, reconstruct it from that day's commits, the files they touched and new inbox files. Say at the top that it was written after the fact. A day with nothing gets a short entry saying so. Never invent.

STEP 2, WEEKLY: previous ISO week = TZ=<TIMEZONE> date -d '7 days ago' +%G-W%V. If 02-journal/weekly/<week>.md is missing, run every step of reviews.md "Weekly", including the due evaluations in 00-system/learning/organization-log.md.

STEP 3, MONTHLY: previous month = TZ=<TIMEZONE> date -d "$(TZ=<TIMEZONE> date +%Y-%m-01) -1 day" +%Y-%m. If 02-journal/monthly/<month>.md is missing, run every step of reviews.md "Monthly" (health check, optimize, promote, thin, at most 1 to 2 backlog items, quarterly look outside). Propose big restructurings to the owner instead of doing them.

STEP 4, HEARTBEAT, ALWAYS: in 00-system/sync/state/automation-runs.json, key "journal": last_run = current UTC ISO time only on success (leave it untouched on failure); status ok or failed; note one short line. Commit it either way.

FINISH
python3 00-system/scripts/linkcheck.py --orphans must exit clean. Check deletions: git diff --cached | grep "^-" | grep -v "^--- ". Check for secrets and misplaced confidential content before committing. Commit message says what and why. Never rewrite pushed history. Final report: files created, steps skipped and why, evaluations closed, heartbeat written, contradictions found.
```

## Example prompt: nightly inbox triage

```text
You are the scheduled nightly inbox triage for this Second Brain repository. Nobody is watching: work autonomously, finish, push, ask nothing.

RULES
1. Read AGENTS.md and CLAUDE.md first; they and .claude/rules/ are binding. The repository wins over this prompt; report any contradiction.
2. No worktree. Work on main, commit, push (exception in 00-system/workflows/automation.md).
3. Follow 00-system/workflows/triage.md. It overrides this prompt if the two disagree.
4. Step 0: check that every path named here exists. Name any missing one in the heartbeat note and in 00-system/learning/observations.md.

CHECKOUT
The checkout may be shallow and local main may be stale. "refusing to merge unrelated histories" is a shallow-clone artifact. With a clean tree: git fetch origin main, git switch --detach origin/main, and at the end git push origin HEAD:main.

STEP 1, BRANCHES: run python3 00-system/scripts/branch_overview.py --fetch. Do not merge branches. Before touching a file it reports as a collision, read the other branch's version.

STEP 2, TRIAGE: if 01-inbox/ holds only README.md, there is nothing to do; go to step 3. Otherwise process every capture per triage.md: split mixed captures by topic, search before create, update canonical files, link every filed item from the file that owns its topic, delete processed captures. An undecidable capture stays in the inbox with a one-line note: never guess. A value that needs a look at an original document you cannot open stays in the inbox too. Update touched indexes and 00-system/current-context.md.

STEP 3, HEARTBEAT, ALWAYS (also on an empty inbox or a failed run): in 00-system/sync/state/automation-runs.json, key "triage": last_run = current UTC ISO time only on success (leave it untouched on failure); status ok or failed; note one short line. Commit it either way.

FINISH
python3 00-system/scripts/linkcheck.py --orphans must exit clean. Check deletions: git diff --cached | grep "^-" | grep -v "^--- " (only processed captures may be deleted). Check for secrets and misplaced confidential content before committing. Commit message says what and why. Never rewrite pushed history. Final report: captures processed and where they went, captures left and why, heartbeat written, contradictions found.
```

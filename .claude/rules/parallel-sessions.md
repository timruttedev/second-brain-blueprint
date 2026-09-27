# Rule: Multi-Session Mode

Applies only when AGENTS.md says `Mode: multi-session`
([operating mode](../../AGENTS.md#operating-mode)). In single-session mode,
ignore this file: work on `main`.

**Every session works in its own Git worktree on its own branch.** Never in
the main checkout. Why: two sessions sharing one directory silently
overwrite each other's files, and Git does not warn.

## Procedure

1. **At the start**, before the first write: `git fetch`, then
   `EnterWorktree(name: "<topic>")` (name by topic, not date), then
   `git merge origin/main` **inside the worktree**. Never merge in the main
   checkout: another session may be using it. If the session already runs
   in a worktree (`git rev-parse --git-dir` differs from
   `--git-common-dir`), do not create a second one.
2. **During the work,** commit in small complete units. `git add -A` is
   fine: the worktree holds only your own work.
3. **Before creating any new canonical file:** `git fetch`, then
   `git merge origin/main`, and check unmerged branches with
   [branch_overview.py](../../00-system/scripts/branch_overview.py). Why:
   otherwise "search before create" misses a file a parallel session just
   created. `git merge main` is not enough: it compares against your local
   `main`, which may be behind and report "Already up to date".
4. **At the end:** `git fetch` and `git merge origin/main` into the branch.
   Resolve conflicts there. Keep branches short-lived: a branch open for
   days collects exactly the conflicts this mode avoids.
5. **Push the branch and open a pull request** when the first draft stands
   ([pull requests rule](./pull-requests.md)). Merge through the pull
   request, not by hand in the main checkout. Push intermediate states
   whenever there is something to upload.
6. **After the merge:** `ExitWorktree`, remove the worktree, delete the
   branch.

## In a shared tree

- **Never use `checkout`, `reset`, `stash` or `rebase` to tidy up** a tree
  you did not create. If someone else's uncommitted work blocks a merge,
  wait, or cut your change so it does not touch the contested file.
- **Touch hub files last:** `00-system/current-context.md` and
  `00-system/indexes/*` are the likeliest conflicts. Append-only logs are
  uncritical.
- **If `EnterWorktree` fails** (sandbox, permissions): say so and continue
  in the main checkout. Read `git status`, stage strictly by path (never
  `git add -A`), leave other people's changes untouched.

Scheduled cloud runs are the exception: they work on `main` in their own
checkout ([automation](../../00-system/workflows/automation.md)).

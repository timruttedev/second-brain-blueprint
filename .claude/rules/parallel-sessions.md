# Rule: Every Session Works in a Worktree

How sessions stay isolated from each other, and the checks before every
commit.

**Every session works in its own Git worktree on its own branch.** Never
directly in the main checkout, unless the owner explicitly says otherwise.

Why: two sessions sharing one directory silently overwrite each other's
files, and Git does not warn about it.

## Procedure

1. **At the start**, before the first write: `git fetch` and
   `git merge origin/main` in the main checkout, then
   `EnterWorktree(name: "<topic>")`. Name worktrees by topic, not by date.
   If the session already runs in a worktree (`git rev-parse --git-dir`
   differs from `--git-common-dir`), do not create a second one.
   Why fetch: whatever the local checkout does not know does not exist for
   the session, and scheduled runs write to `origin/main` on their own.
2. **During the work**, commit normally in small complete units.
   `git add -A` is fine here: the worktree holds only your own work.
3. **Before creating any new canonical file:** `git fetch`, then
   `git merge origin/main`. Also check unmerged branches with
   [branch_overview.py](../../00-system/scripts/branch_overview.py).
   Why: otherwise "search before create" misses a file that a parallel
   session just created, and you write a duplicate. Note that
   `git merge main` alone is not enough: it compares against your **local**
   main. If that is behind, the merge reports "Already up to date" and you
   miss work.
4. **At the end:** `git fetch` and `git merge origin/main` into the branch.
   Resolve conflicts there, not on main. Keep branches short-lived: a
   branch that stays open for days collects exactly the conflicts this
   model is meant to avoid.
5. **Push the branch and open a pull request** as soon as the first draft
   stands ([pull requests rule](./pull-requests.md)). Merging happens
   through the pull request, not by hand in the main checkout.
6. **After the merge:** `ExitWorktree`, remove the worktree, delete the
   branch. Never rewrite published history.

**Pushing needs no occasion.** Push the branch whenever there is something
to upload, including intermediate states. The checks below stay where they
are: **before the commit**.

## Pre-commit checks

- **Never use `checkout`, `reset`, `stash` or `rebase` to tidy up** a tree
  you did not create. If someone else's uncommitted work blocks a merge,
  wait, or cut your own change so it does not touch the contested file.
- **Touch hub files last:** `00-system/current-context.md` and
  `00-system/indexes/*`. They are the most likely source of conflicts.
  Append-only logs are uncritical.
- **Run the link checker before the commit**, not at the next health check:

  ```bash
  python3 00-system/scripts/linkcheck.py --orphans
  ```

  Exit 1 means a link, anchor, `type:` value, frontmatter field or code
  fence does not resolve, a file exceeds its `max_lines`, or an evaluation
  in the organization log is due. Fixing it in the same session is cheap,
  days later it is expensive. The checker guards itself with a
  [canary](../../00-system/scripts/canary.md): a deliberately broken link it
  must find, so a broken checker cannot report "all green".
- **Scan the diff for deletions:**

  ```bash
  git diff --cached | grep "^-" | grep -v "^--- "
  ```

  An additive change must not contain deletions. Do not use
  `grep "^-[^-]"`: it hides deleted Markdown bullet lines (`-- item`), which
  are the most common line in a knowledge base.
- **Scan the diff for style violations.** If the owner has a style rule
  that can be expressed as a pattern (a banned character, a banned word),
  grep the added lines for it:

  ```bash
  LC_ALL=C.UTF-8 git diff --cached | grep "^+" | LC_ALL=C.UTF-8 grep -P "<pattern>"
  ```

  Keep the `LC_ALL=C.UTF-8`. Why: under a `POSIX` locale, `grep -P` compares
  bytes instead of characters, and multi-byte characters that share a first
  byte produce false hits. Every hit is either text to rewrite or a
  documented exception (a verbatim quote, a delimiter in a documented line
  format).
- **Check for secrets and misplaced sensitive content.** A push publishes,
  and this is the last gate
  ([privacy and security](./privacy-security.md)).

## Scheduled runs in the cloud

Scheduled runs (for example a morning journal run and a nightly inbox
triage, see [automation](../../00-system/workflows/automation.md)) may work
**without a worktree**, directly on `main`: they commit and push.

Why this is safe: each run gets its own fresh checkout that shares no
directory with any other session, so the isolation this rule creates
already exists. Space the runs hours apart so they do not write to the same
file at the same time.

This exception holds **only** for one session in its own checkout with
nobody typing next to it. As soon as a run lands in a shared directory, the
procedure above applies again.

## When isolation is impossible

If `EnterWorktree` fails (sandbox, permissions): **say so** and continue in
the main checkout. Then read `git status`, stage strictly by path (never
`git add -A`), and leave other people's changes untouched.

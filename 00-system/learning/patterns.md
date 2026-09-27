# Patterns

Confirmed, durable patterns that agents honor in daily work.

A new pattern is promoted from the observations (the month files behind
[observations.md](./observations.md)) only with enough evidence: about 3
independent occurrences, or one explicit confirmation by the owner. Patterns cover things like work preferences,
preferred presentation, recurring relations between topics, recurring
project structures and recurring workflows.

## Format

Every pattern, seed or your own, uses the same shape:

```
## <short name>

- **Pattern:** what holds
- **Why:** what goes wrong without it
- **How to apply:** what agents do differently (a sub-list is fine)
- **Evidence:** dated occurrences or the owner statement (optional for
  seed patterns, required for your own)
```

When a pattern changes, add a dated line under it
(`Revised YYYY-MM-DD: old -> new, because ...`). If it stops holding, mark
it `Superseded YYYY-MM-DD` with the reason. Do not delete it silently.

## Seed patterns

The patterns below ship with the blueprint. They are generic lessons from
running a system like this one. Keep them, adapt them, or mark them
superseded when your own evidence says otherwise. Your own patterns go
below the seed patterns and above the "Advanced" section, in the format
above. The "Advanced" section at the end holds seed patterns that only
matter in some setups (scanned documents, cloud checkouts).

---

## A rule that no mechanism checks does not hold

- **Pattern:** Conventions get broken by sessions that **know** them. Where
  a rule can be written as a command, the command is the rule and the text
  next to it is only the reason.
- **Why:** Stronger wording is the wrong lever. An agent that does not
  apply a convention will not apply a louder version of it either. A cleanup
  without a check only produces the next round.
- **How to apply:**
  - Before writing down a convention about form, metadata or filing, ask:
    can the same sentence be a check? If yes, build the check and keep the
    text as its reason.
  - Put the check where the work happens (the
    [pre-commit checks](../../AGENTS.md#pre-commit-checks)), not only
    where the rule is explained. A consequence that lives only in the
    explanation does not get run.
  - Limit: content rules (what counts as fact, what the owner decides)
    cannot be checked mechanically and stay text.

## A check that silently reports green is worse than none

- **Pattern:** Monitoring rarely fails loudly. It stops checking and keeps
  reporting success.
- **Why:** Without a check you look yourself. With a green report you stop
  looking, so the damage is the false trust, not the gap.
- **How to apply:**
  - Every check needs proof that it still checks. For `linkcheck.py` that
    is the [canary](../scripts/canary.md): a deliberately broken link every
    full run must find, or the run exits 2.
  - When building a monitor, first ask: what does its failure look like? If
    the answer is "like success", it is not finished. No skip without a
    message, no `continue` without a count, no empty result that looks like
    "nothing found".
  - Test a search pattern against a real hit. Create the case it should
    catch once and see it reported. An untested pattern is a claim, not a
    check.
  - A check that measures presence says nothing about effect. "The code is
    in the file" does not mean it runs.

## Search before create, including other branches

- **Pattern:** Before creating a canonical file, search for an existing
  home. When more than one branch exists (multi-session mode, scheduled
  runs), the search includes unmerged branches, not just the working tree
  and `main`.
- **Why:** A duplicate splits one fact into two places that drift apart.
  Work that is finished but unmerged is invisible to a session that only
  reads `main`, so it gets built a second time, often differently.
- **How to apply:**
  - Bring your checkout up to date before creating a canonical file:
    `git pull` on `main`, or `git fetch` and `git merge origin/main` on a
    branch. `git merge main` alone compares against a possibly stale local
    branch and reports "Already up to date".
  - When branches exist, run
    `python3 00-system/scripts/branch_overview.py --fetch` before triage
    and before creating canonical files. If it reports a file on
    another branch, read it there (`git show <branch>:<path>`) before
    writing.
  - Update the existing file and link to it instead of copying.

## Uncertain readings stay uncertain

- **Pattern:** Facts read from scans are often partly illegible, undated or
  ambiguous. Record what the document says plus the doubt, never the
  likelier guess.
- **Why:** A guessed value looks settled and blocks its own correction. A
  marked value gets closed by the next document. Flagging doubt is only
  half the rule; the other half is not resolving it from plausibility.
- **How to apply:**
  - Write the reading, name the uncertainty, date the source.
  - Only the owner or a later document closes the doubt, not an agent's
    reasoning about what is likely.
  - Keep old values as history: the chain of documents, not any single
    one, is what surfaces an error.

## Update in place, keep the history

- **Pattern:** The newest explicit owner statement defines the current
  state. Earlier values stay as dated history.
- **Why:** A silently overwritten fact cannot answer "since when?" or
  "why did this change?". A file full of stale values cannot answer "what
  is true now?". Both questions need to work.
- **How to apply:**
  - Update the current statement in place and add a short history line:
    `2030-01-01: A -> 2030-06-01: B`.
  - Mark a corrected assumption as corrected, do not erase it.
  - Documents the owner hands over are snapshots: never rewrite the
    owner's text. Mark it (truncated, superseded) and point to what is now
    authoritative. When a whole document is replaced, keep a small change
    table (old reading, new reading).

## Routines: status is not effect, the heartbeat is

- **Pattern:** A scheduled run can report success and change nothing. The
  only proof of effect is a commit it made.
- **Why:** A routine's status says the run finished, not that it did its
  job. A heartbeat described in a workflow but missing from the routine
  prompt looks exactly like health.
- **How to apply:**
  - Every scheduled run writes a heartbeat to
    `00-system/sync/state/automation-runs.json` (time, status, one-line
    note) and commits it, even when there was nothing to do.
  - Judge a routine by its heartbeat commit, never by the status in the
    scheduler UI.
  - The routine prompt lives outside the repository and nothing checks it.
    Change the prompt first, then the docs, and keep the prompt short: it
    points to the workflow docs, which override it.

## A process that proves itself gets scheduled

- **Pattern:** Once a recurring workflow has worked by hand twice, running
  it by hand stops being worth it. Manual runs are the trial phase.
- **Why:** A workflow that depends on someone remembering to start it
  quietly stops happening.
- **How to apply:**
  - At the second manual run, offer a schedule. The question is not
    "should this be automated?" but "at what time?".
  - A scheduled run needs an idle answer. Most nights there is nothing to
    do; the prompt must treat that as normal and end without noise (only
    the heartbeat).
  - A scheduled run must not guess. Nobody can answer a question at night.
    Unclear items stay where they are, marked.
  - Stagger the times. Every run writes to `main`; give each one its own
    slot so two runs never write the same file at once.

## Specs and plans are session material, not committed

- **Pattern:** Design documents, implementation plans and task lists stay
  out of version control.
- **Why:** A plan describes what someone intends and is worthless once
  done. A decision describes why something is the way it is and is needed
  for years. Committing plans buries the second under the first.
- **How to apply:**
  - Write plans in the session's scratch directory. If one must live in the
    project folder, add its path to `.gitignore`.
  - What turned out to be durable during the work goes into the durable
    home: a decision record, a workflow, a knowledge file, a README.

## In multi-session mode, a task ends with a pull request

- **Pattern:** Applies only when the operating mode in `AGENTS.md` is
  multi-session. A new task is not done with a push. As soon as the first
  draft stands (built, checked, presentable), open a pull request without
  being asked.
- **Why:** The pull request is where the owner reviews work: diff, checks
  and description in one place. A branch without one makes them go
  searching, and unmerged branches are invisible to later sessions.
- **How to apply:**
  - Whatever is still open goes into the pull request text, not into a
    delayed pull request.
  - A follow-up on a branch whose pull request is already open needs no
    second one.

## Identifying values go in, document copies stay out

- **Pattern:** The line is not "sensitive versus harmless" but "value
  versus document copy". Facts and identifiers (birth dates, tax IDs,
  registry numbers) belong in the repository, marked `confidential`. Scans
  and photos of official documents do not.
- **Why:** The value is what retrieval needs; the scan adds risk and bulk
  without adding knowledge. Secrets are different again: they authenticate
  rather than identify and are never stored.
- **How to apply:**
  - Record identifying values without asking each time, with
    `sensitivity: confidential` in the frontmatter.
  - Keep scans in an external document store and reference them.
  - Never store passwords, keys, tokens or PINs; store where they live
    instead.

---

# Advanced

Seed patterns for specific setups. Skip them if they do not apply to you.

## Never trust an OCR text layer for values that matter

- **Pattern:** Scanners embed their own OCR. A PDF that returns text is no
  evidence that the text is right.
- **Why:** OCR is confidently wrong in small ways (a digit, a letter in an
  IBAN or BIC, a word) and drops handwriting (dates, signatures, filled-in
  fields) entirely.
- **How to apply:**
  - Read every name, number, amount, date and signature field off the
    **image** before recording it.
  - A value stated twice in the document checks itself. If the two copies
    disagree, the OCR is wrong, not the issuer.

## Shallow clones report "unrelated histories"

- **Pattern:** Cloud checkouts are often shallow clones. Across the shallow
  boundary Git finds no common ancestor and reports `refusing to merge
  unrelated histories`, although one exists.
- **Why:** It looks like rewritten history and tempts a destructive fix
  (`reset --hard`, force push). Usually nothing is wrong except the missing
  depth.
- **How to apply:**
  - Check with `git rev-parse --is-shallow-repository` before concluding
    anything.
  - If allowed, `git fetch --unshallow origin main`, then retry.
  - `branch_overview.py` lists branches it could not compare for this
    reason as skipped, never as "all clear"; `--fetch` tries to deepen.
  - Otherwise work from a fresh state without destroying the old one:
    `git switch --detach origin/main`, commit, `git push origin HEAD:main`.
    Never rewrite pushed history to "fix" it.

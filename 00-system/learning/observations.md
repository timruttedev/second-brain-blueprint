# Observations

Short-lived, dated signals about how the system is (or is not) working.
Newest first. **Not every observation becomes a rule.**

Entries live in [`observations/`](./observations/), one file per month.
This file is only the signpost. A new observation goes into the file for
the current month; if that file does not exist yet, create it and add a row
here.

| Month | File |
|---|---|
| _none yet_ | _create `observations/YYYY-MM.md` with the first entry_ |

## What to capture

- The owner searches for the same topic repeatedly.
- Two categories are always needed together.
- A template creates busywork.
- A kind of information keeps getting misfiled.
- A file is repeatedly hard to find.
- The owner corrects the same assumption more than once.
- A check or a scheduled run failed silently.

## Format

```
- YYYY-MM-DD: observation (context; count if repeated: 2x, 3x ...)
```

Example (not a real entry):

```
- 2030-01-15: Recipes were filed under 06-knowledge/ twice and under
  04-areas/ once (3x). Candidate for a pattern or a taxonomy note.
```

## Length and thinning

- Length follows the evidence, not a line limit. Say what happened, what it
  cost, and how often it has happened now.
- What keeps the log usable is thinning, not brevity. At the monthly review
  remove entries that were promoted, done, or are clearly stale, with one
  line saying where each went. Git keeps what was removed.
- Why: a log nobody thins turns into a chat archive and stops being read.

## Watch the relative paths

The month files sit one level deeper than this file. From
`observations/YYYY-MM.md`, `00-system/` is `../../` and the repository root
is `../../../`. Links to siblings inside `learning/` are `../patterns.md`.
Run `linkcheck.py` before committing; it catches a wrong depth.

# Organization Log

Append-only log of **significant structural changes**, not every small file
move. Newest first.

Entries live in [`organization-log/`](./organization-log/), one file per
month. This file is only the signpost. A new entry goes at the top of the
file for the current month; if that file does not exist yet, create it and
add a row here.

| Month | File |
|---|---|
| _none yet_ | _create `organization-log/YYYY-MM.md` with the first entry_ |

## Entry format

```
## YYYY-MM-DD: short title

Observation: what prompted this
Change:      what was changed
Reason:      why this improves the system (against the optimization priorities)
Result:      outcome, filled in at the next review (keep / modify / revert),
             open only WITH a review date: '_open, review on YYYY-MM-DD._'
Reversible:  yes / partly / no
```

## Open results are checked

- `linkcheck.py` reads every `Result:` line in `organization-log/`.
- An open entry is **due** once its review date is reached. If it names no
  date after its heading date, it is due 30 days after that heading date.
- Both are closed by the same move: write a verdict (keep / modify /
  revert) or set a concrete review date.
- Why: "check at the next review" is not a deadline, it is the absence of
  one. Without the check, most results stay open forever and the loop never
  learns whether a change worked
  ([Pattern](./patterns.md#a-rule-that-no-mechanism-checks-does-not-hold)).

Reverting a failed change is the system learning, not a failure. Record it
as `Result: revert` with the reason.

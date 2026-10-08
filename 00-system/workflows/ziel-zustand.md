# Workflow: Goal and state layer

The layer between the knowledge base and the agents that act. It turns
context that is already in the repository into one next step. It does not
ingest new sources, and it does not execute.

Canonical for every agent. A skill may wrap this file later. If the two
diverge, this file wins.

Start with one domain. Further domains get a `steuerung/` folder (steering)
only when a pilot for them is actually started. The folder lives in the
owning area.

## The loop

```
signal
  -> update state from the canonical files
  -> compare with goals
  -> derive one next step
  -> check permission
  -> suggest, or do what is already allowed
  -> measure
  -> write the outcome back
```

## Files, per domain

| File | Holds | Does not hold |
|---|---|---|
| `state.md` | What is true now: active items, blockers, progress, a few figures, the single largest gap | History, contact details, amounts that already live in a canonical file |
| `goals.md` | Outcomes with horizon and a test for "achieved?" | A second copy of `indexes/goals.md` |
| `priorisierung.md` | The working rules, and exactly one dated recommendation | A backlog of equal-priority tasks |
| `feedback.md` | Overrides with the owner's reason, the override rate, hypotheses | A new standing rule |

`README.md` in the same folder says which permissions apply in that domain.

Headline goals stay in `indexes/goals.md`. The domain file holds the
outcomes that steer planning, with a link back.

## State rules

- The state is a compiled view. On any conflict the canonical file wins,
  and the state is corrected in the same change.
- One line points at the source. A figure is copied only when the planning
  question cannot be answered without it.
- Facts from a `confidential` or `restricted` file stay behind the link,
  except the one status the planning question needs.
- `updated:` is the day the view was checked against its sources, not the
  day a source file happened to change.
- Give `state.md` a `max_lines` budget. Compactness is the point. Raise
  the number only in the same commit that explains why the view had to grow.

## One next step

Compare the goals with the state. Name the largest gap that the owner can
actually move this week. Recommend the smallest action that narrows it.

Rules of the first version, until a later decision replaces them with a
score:

1. Prefer an action the owner can take over one that is waiting on someone else.
2. Prefer a concrete open loop over starting a new workstream.
3. A clear mismatch is a short decision, recorded where that item already lives.
4. Publish exactly one recommendation. Everything else is a queue, ordered,
   not a second recommendation.

Date the recommendation. Replace it when the owner answers or when a source
fact it depends on changes. Keep the previous recommendation as one history
line, so the feedback log can point at it.

## Permission

Three levels. The domain README states which actions sit where. The default
for anything that leaves the repository (a message, an offer, a price, a
commitment) is **suggest**.

| Level | Agent may |
|---|---|
| Suggest | Update the state, name the next step, draft text in the chat |
| After a yes in the same conversation | File the owner's decision into the canonical file, keep the draft they accepted |
| Autonomous | Only what a decision already allows. Nothing that leaves the repository is in this level |

Doing the recommended action is not implied by writing it down.

## Feedback and learning

When the owner accepts, rejects or changes a recommendation, append one
entry to `feedback.md`: the proposal, their choice, their reason in their words.

- One case is evidence. It does not become a rule.
- The same reason, about three times, becomes a **hypothesis** in that
  file. Say so in the entry.
- A hypothesis becomes a decision record only when the owner confirms it,
  through [decision-record.md](./decision-record.md).

The measure is the **override rate**: among recommendations they have
answered, the share they reject or materially change. Unanswered
recommendations do not count. Record it by week. A falling rate over
several weeks is the signal that the rules match them better. One week is
not a trend.

## When to update

- A session that changes a fact the state links to updates the state in
  the same session, if the fact changed what is true now.
- The weekly review refreshes a pilot whose linked files changed that week
  ([reviews.md](./reviews.md)).
- Do not refresh on a schedule when nothing moved. A dated "checked, no
  change" line is enough.

## What this version leaves open

No numeric score. No timetable. No autonomy for actions that leave the
repository. No separate service: the first version is Markdown in Git,
because that is already the canonical store. Those four points stay open
until the owner decides them.

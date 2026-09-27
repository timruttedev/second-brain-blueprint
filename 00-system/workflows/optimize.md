# Workflow: Optimize (whole-system review)

Purpose: a periodic step back to judge the whole system, typically at the
monthly review or on request. It complements
[system-health-check.md](./system-health-check.md) (mechanical criteria)
with judgment questions.

## Questions

- Is the taxonomy still right? Types nobody uses? Types missing?
- Which folders are barely used (dead categories)? Which are getting too big
  (split candidates)?
- What is repeatedly hard to find? Where do duplicates keep appearing?
- Which information is often read together (co-location or index candidate)?
- Which templates produce dead-weight sections?
- Are agent instructions redundant or bloated (AGENTS.md, CLAUDE.md,
  `.claude/rules/`)? Do skills overlap?
- Which indexes are missing? Which earn nothing?
- Which areas have grown enough to deserve structure? Which structures can
  be simplified?

## Then

1. **Low-risk improvements: do them now**, following
   [reorganization.md](./reorganization.md).
2. **Bigger ideas with unclear benefit: park them** in
   [`optimization-backlog.md`](../learning/optimization-backlog.md). Do not
   act yet.
3. **Log significant changes** in the current month's file in
   [`organization-log/`](../learning/organization-log/) with a review
   date; evaluate them later ([learning-loop.md](./learning-loop.md)).

Evolution over revolution: a small improvement per real problem beats a new
folder structure every month. The system should become **more** stable over
time, not less.

## Look outside, once a quarter

Everything above judges the system by its own observations. That finds
friction, but never a better way that nobody here has seen yet. So once a
quarter, the monthly reviews written in January, April, July and October
(covering December, March, June and September) run one outward step
([reviews.md](./reviews.md#monthly), last step).

1. **Research, dated sources only** (web search; note the date of every
   source and skip anything older than twelve months). Two questions:
   - What is new in the agent tooling this repository uses (for Claude
     Code: skills, hooks, routines, memory, `AGENTS.md` and `CLAUDE.md`
     conventions, context handling) that touches how this repository works?
   - What do current write-ups on AI-assisted personal knowledge systems
     recommend for capture, retrieval, review and self-maintenance?
2. **Match against real problems.** A finding counts only if it would solve
   something already on record: an observation, a pattern, a backlog entry
   or a failing health criterion. Name that entry. "Everyone does it now" is
   not a reason; the optimization priorities in
   [AGENTS.md](../../AGENTS.md) are the yardstick.
3. **Write at most three entries** into
   [`optimization-backlog.md`](../learning/optimization-backlog.md), each
   with source and date, the problem it would solve here, the smallest
   version of it, and a condition under which it becomes worth doing.
   **Nothing is changed in this step.** A later monthly run may implement an
   entry once its condition holds (one or two per month at most); anything
   large goes to the owner.
4. **Nothing worth recording is a valid result.** Say so in one line in the
   monthly note, with the date of the search, so the next quarter knows it
   ran.

Why quarterly and never directly: the system should get more stable over
time, not chase each new recommendation. A quarterly look tied to a known
problem keeps it current without churn.

# Example: a filled-in Second Brain

> **Everything in this folder is fictional.** Alex Morgan, Robin, Jordan Lee,
> the contractors, the amounts and the dates are invented to show how the
> blueprint looks in use. Any resemblance to real people or companies is
> coincidental.

Alex Morgan is a product manager who started a Second Brain in September
2026. This folder is a snapshot of it on **2026-10-16**, two weeks into a
kitchen renovation and a shoulder rehab. It uses the same layout as the
blueprint itself, so every file here shows what the empty template next
door turns into. The setup script deletes this folder unless you pass
`--keep-examples`.

## Start where an agent starts

An agent answering a question reads narrow to broad. Try it yourself with
*"What is open for the kitchen?"*:

1. [`00-system/current-context.md`](00-system/current-context.md) names the
   kitchen as the current focus and links the project.
2. [`00-system/indexes/todos.md`](00-system/indexes/todos.md) shows the
   deadline (2026-10-23) and what blocks it.
3. [`03-projects/kitchen-renovation.md`](03-projects/kitchen-renovation.md)
   has the details: the quote table, the open question, the next steps.

Three small files, and the agent never had to open the journal.

## What each file demonstrates

| File | Demonstrates |
|---|---|
| [`00-system/current-context.md`](00-system/current-context.md) | A signpost: one line and one link per entry, no numbers that live elsewhere |
| [`00-system/indexes/projects.md`](00-system/indexes/projects.md) | Index line format: name, status, next step |
| [`00-system/indexes/areas.md`](00-system/indexes/areas.md) | Areas created from real use, not upfront (only two) |
| [`00-system/indexes/people.md`](00-system/indexes/people.md) | Only people with an active connection |
| [`00-system/indexes/decisions.md`](00-system/indexes/decisions.md) | Decision list, newest first, with status |
| [`00-system/indexes/goals.md`](00-system/indexes/goals.md) | Goals point to their owning file; a paused goal stays listed |
| [`00-system/indexes/todos.md`](00-system/indexes/todos.md) | The one task list: deadlines, blockers, a done item struck through |
| [`00-system/learning/observations/2026-10.md`](00-system/learning/observations/2026-10.md) | Three signals: one led to a change, one to a pattern, one is only watched |
| [`00-system/learning/organization-log/2026-10.md`](00-system/learning/organization-log/2026-10.md) | A structural change with an open result and a concrete review date |
| [`00-system/learning/patterns.md`](00-system/learning/patterns.md) | An own pattern, promoted with evidence and an owner statement |
| [`01-inbox/`](01-inbox/) | Two raw captures waiting for triage: one typed on the phone without frontmatter, one with |
| [`02-journal/daily/2026-10-07.md`](02-journal/daily/2026-10-07.md), [`2026-10-09.md`](02-journal/daily/2026-10-09.md) | Dailies: short, only sections that have content, links to canonical files |
| [`02-journal/weekly/2026-W41.md`](02-journal/weekly/2026-W41.md) | A weekly review that condenses instead of copying |
| [`03-projects/kitchen-renovation.md`](03-projects/kitchen-renovation.md) | A one-file project: definition of done, open loops, a comparison table, a log |
| [`04-areas/health.md`](04-areas/health.md) | An area with current state, a goal and dated history |
| [`04-areas/finances.md`](04-areas/finances.md) | `sensitivity: confidential`, and a changed value kept as history |
| [`05-people/jordan-lee.md`](05-people/jordan-lee.md) | A person file limited to what matters for Alex's projects |
| [`06-knowledge/induction-cooktops.md`](06-knowledge/induction-cooktops.md) | General knowledge kept apart from personal context, with a label |
| [`07-decisions/2026-10-11-induction-instead-of-gas.md`](07-decisions/2026-10-11-induction-instead-of-gas.md) | A decision record with reasons and rejected alternatives |

## Before and after triage

On the evening of 2026-10-08, Alex dictated this capture into the phone. It
landed as `01-inbox/2026-10-08-2215-jordan-kitchen.md`:

```text
jordan was here, looked at the plans and quote B. B forgot the ducting for
the extractor hood, ask them!! jordan says induction is a no brainer if we
redo the wiring anyway. electrician needs to check the circuit first.
jordan's birthday is 14 nov btw. physio moves to tuesdays for the rest of oct
```

One capture, five facts, four different homes. Triage on 2026-10-09 split
it like this, then deleted the capture (Git keeps the original):

| Piece of the capture | Where it went | Why there |
|---|---|---|
| B forgot the ducting, ask them | [Project](03-projects/kitchen-renovation.md#open-loops): open loop, next step, log entry; the question to B was sent the same day ([daily](02-journal/daily/2026-10-09.md)) | It is about the project; the repository does not know the answer yet |
| Induction is a no brainer | Input for the [decision](07-decisions/2026-10-11-induction-instead-of-gas.md), taken two days later, and a [knowledge note](06-knowledge/induction-cooktops.md) on what induction requires | Jordan's opinion is a reason, not yet a decision; the general facts stand on their own |
| Electrician must check the circuit | [To-do index](00-system/indexes/todos.md#blocks-something-else) | A task with a consequence: it blocks the contract |
| Jordan's birthday | [Person file](05-people/jordan-lee.md), plus the interaction of 2026-10-08 | A fact about a person who matters for an active project |
| Physio moves to Tuesdays | [Health](04-areas/health.md): current state and history | Changes a current value; the old one stays as history |

Nothing was copied twice: the index and the current context got one line
and one link each, the details live in one place.

**Try it:** the two captures still in [`01-inbox/`](01-inbox/) are waiting.
The physio note updates the health area and closes nothing yet; the
standing transfer idea belongs to the finances area and waits for the new
account. Ask your agent how it would triage them, without changing any
files, and compare its answer with this reasoning.

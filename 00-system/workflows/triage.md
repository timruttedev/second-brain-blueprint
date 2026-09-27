# Workflow: Triage

Purpose: turn inbox captures (and durable content stuck in daily notes) into
canonical knowledge. Run when asked, as part of the weekly review, or nightly
as a [scheduled routine](./automation.md). The inbox should tend toward
empty.

## Step 1: check what is sitting on branches

Before anything else, in every run:

```bash
python3 00-system/scripts/branch_overview.py --fetch
```

It lists every remote branch that `main` does not contain: age, commits,
changed files, and the files that are touched on **several** branches at
once.

Why: the inbox is not the only place where unprocessed work waits. A capture
on an unmerged branch is invisible to a triage on `main`, and two branches
can file the same capture in two different places without seeing each
other.

The result is a precaution, not a task: branches are not merged here. Before
touching a file the script reports as a collision, read the other branch's
version (`git show <branch>:<path>`). Before creating a canonical file,
check that no branch already has it.

## Step 2: split a collective capture

**A capture is not always one topic.** Voice notes, meeting notes and
evening recaps often carry several independent subjects that belong in
different canonical files. The questions below assume one capture about one
thing; applied to a mixed capture, they produce one compromise destination
instead of three correct ones.

So: read the capture, list its topics, and run the questions **per topic**.
Delete the capture once, after the last topic is filed.

## Step 3: per item, ask in this order

**Search first** (rg, globs, indexes), then:

1. Does this knowledge already exist? → update the canonical file (keep a
   dated history line if it changes current state), delete the capture.
2. Does it belong to an existing project? → into that project file.
3. Does it belong to an area? → into that area file.
4. Is it a decision? → decision record in `07-decisions/`
   ([decision-record.md](./decision-record.md)).
5. Is it just an event? → into the daily note for that date.
6. Is it durable knowledge? → `06-knowledge/` (separate general knowledge
   from personal context).
7. Is it a task or open loop? → into the owning project's or area's open
   loops; headline loops also into
   [`current-context.md`](../current-context.md).
8. Is it only temporarily relevant? → leave it in the daily note; do not
   create a permanent file for it.
9. Does it contradict existing knowledge? → resolve it per AGENTS.md
   ("Conflicting information"): the newest explicit statement wins, history
   is kept.

**Create a new file only when no existing canonical home makes sense.** If
several captures point at an emerging topic, that may be the birth of a new
project or area: create it, add it to the index, and note the signal in
[`observations.md`](../learning/observations.md).

Every filed item must be **linked from the file that owns its topic**
([capture.md](./capture.md#filing-is-only-half-connect-it)).

### A conversation file does not replace the canonical update

For long conversation captures, a dated file in the owning area
(`04-areas/<area>/YYYY-MM-DD-topic-conversation.md`) is a good home for
**history and reasoning**: who said what, which hypothesis was dropped, what
was only the assistant's assessment.

It is **not** a substitute for question 1. Whatever holds durably after the
conversation also goes into the canonical file, with date and source: a
commitment into the strategy or area file, a decision into `07-decisions/`,
a task into the open loops. The conversation file is the evidence; it does
not own the fact.

The test before deleting the capture: **can someone who does not know the
date of the conversation find the result?**

### Machine-extracted captures

Captures from an ingest pipeline often carry OCR or transcribed text. Read
every value that matters (names, numbers, amounts, dates) off the original
before recording it
([knowledge integrity](../../.claude/rules/knowledge-integrity.md)). If the
original is not reachable in this session, leave the capture in the inbox
with a one-line note.

## After processing a batch

- Delete processed captures: their content now lives canonically, and Git
  keeps the raw history. Unclear items may stay in the inbox; note repeat
  offenders as friction observations.
- Update touched indexes and [`current-context.md`](../current-context.md)
  if focus, projects or loops changed.
- Record notable friction in [`observations.md`](../learning/observations.md).
- Run `python3 00-system/scripts/linkcheck.py --orphans` before committing.

## When it runs unattended

The nightly routine follows this workflow with three additions (details in
[automation.md](./automation.md)):

- **An empty inbox is the expected outcome** on most nights. The run still
  writes its heartbeat.
- **An undecidable capture stays in the inbox** with a one-line note.
  Nobody is awake to answer a question, and a guess looks settled and blocks
  its own correction.
- **Values that need a look at an original document** that the cloud cannot
  reach stay in the inbox for an interactive session.

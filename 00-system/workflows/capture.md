# Workflow: Capture

Purpose: make capturing a thought near-zero effort. **No filing decisions at
capture time**: no folder, no tag, no category, no target file. The system
decides later, at triage.

## Lifecycle position

```
CAPTURE → INBOX → TRIAGE → CANONICALIZE → CONNECT → USE → REVIEW → ARCHIVE
```

## Convention (conflict-free across devices)

Write **one atomic Markdown file per capture** into `01-inbox/`:

```
01-inbox/YYYY-MM-DD-HHMM-short-slug.md
```

- Timestamp = capture moment (local time). The slug is 2 to 5 words of what
  it is; in a hurry, even `-note` is fine.
- Content: freeform. One line is fine. Any language.
- Optional single header line for context, for example `source: phone`.
- If one day ever produces very many captures, a day subfolder
  `01-inbox/YYYY-MM-DD/` may be used, same naming inside.

Why atomic files: several devices commit to Git at the same time. Unique
timestamped file names never conflict on merge; one shared `inbox.md` does.

## Agent-assisted capture

When the owner tells an agent something worth keeping mid-conversation, the
agent either files it canonically right away (if the home is obvious and the
edit is small) **or** writes an inbox capture. Never let it evaporate with
the chat. Daily notes (`02-journal/daily/`) also count as capture surfaces;
durable content in them still gets canonicalized at triage or review time.

## Filing is only half: connect it

The lifecycle says `CANONICALIZE → CONNECT`, and the second arrow is the one
that gets skipped. **A file that no other file links to is unreachable in
practice**, however well it is named and placed. The retrieval hierarchy
goes context → index → canonical file → linked files, and a file with no
inbound link sits outside all four.

So a filed item is finished only when **the file that owns the topic points
at it**: the area README, the person file, the project, or an index. Add one
sentence saying what is in there, not just a bare link.

The check that finds unconnected files:

```bash
python3 00-system/scripts/linkcheck.py --orphans
```

Orphans are a hint, not an error, and some are legitimate (READMEs, journal,
inbox). A **new content file** among them is not.

## Automated capture (optional)

Ingest pipelines (a scanner, an email filter, a phone shortcut) can drop
captures into `01-inbox/` using the same naming convention, plus a `source:`
line naming the pipeline. The original document (scan, attachment) stays
outside the repository; the capture links to where it lives. Treat any
machine-extracted text (OCR) as unverified until someone checks the values
against the original.

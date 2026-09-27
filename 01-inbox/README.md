# 01-inbox

Unsorted capture buffer. **Zero filing decisions at write time:** just get
it in. Processed via [triage](../00-system/workflows/triage.md); the inbox
trends toward empty.

## Capture convention (conflict-free Git sync)

One atomic file per capture, never one shared big `inbox.md` edited on
several devices:

```
01-inbox/YYYY-MM-DD-HHMM-short-slug.md
```

Example: `2000-01-01-1942-idea-budget-dashboard.md`

- Timestamp = capture moment; slug = 2 to 5 words (in a hurry, `-note` is fine).
- Content is freeform, any language; one line is enough.
- Very busy day? A day subfolder `YYYY-MM-DD/` with the same naming is fine.

Why one file per capture: two devices never write to the same file, so Git
never has to merge a conflict.

## Automated captures

Ingest pipelines (mail, documents, calendars, chat) can drop captures here
when they cannot file something canonically on their own:

```
01-inbox/YYYY-MM-DD-HHMM-<source>-<upstream-id>-<slug>.md
```

- Frontmatter `source: <source>`. The upstream ID keeps the pipeline
  idempotent: it finds its own capture again instead of writing a second one.
- The capture is a **pointer, not a copy**: subject, people involved, dates,
  a reference to the original. The original stays in its own system.
- OCR or extracted text is unverified. Read every value that matters off the
  original before recording it.
- Triage as usual: file the facts canonically with the source noted, then
  delete the capture.

Full workflow: [capture](../00-system/workflows/capture.md).

# Rule: Knowledge Integrity

How to keep facts correct, single and traceable.

- **Search before create.** Update the canonical file instead of writing a
  duplicate. One canonical location per fact: link, don't copy.
- **Never let information vanish.** Content removed from one place must
  reappear in its new home or in `09-archive/`. Verify this in the diff
  before committing multi-file changes.
- **Never present AI inference as the owner's fact.** Label when it
  matters: confirmed fact, user statement, decision, assumption,
  hypothesis, AI suggestion, idea, external information.
- **Uncertain document readings stay uncertain.** When a scan is partly
  illegible, undated or ambiguous, record what it says plus the doubt,
  never the likelier guess. Why: a guessed value looks settled and blocks
  its own correction. A marked doubt gets closed by the next document.
- **Never trust an OCR text layer for a value that matters.** Scanners
  embed their own OCR, so extracted text is no proof the text is right. It
  is often wrong in small ways (a digit, a letter in an IBAN) and drops
  handwriting entirely. Read every name, number, amount, date and signature
  field off the **image** before recording it. A value the document states
  twice checks itself: if the two copies disagree, the OCR is wrong.
- **Medical documents: record, don't select.** Keep every value, including
  normal ones, with unit and reference range. Why: today's normal value is
  the baseline for a later comparison. Check poorly legible results
  visually. A guessed lab value is more dangerous than a missing one.
- **Legal matters: record, don't summarize.** Names, file numbers, amounts,
  deadlines and quotes in full. See
  [privacy and security](./privacy-security.md).
- **Explicit owner statements outrank AI inference.** On conflict, the
  newest explicit statement wins and the superseded version stays as dated
  history.
- **When the owner corrects you, fix the canonical file in the same
  session.**

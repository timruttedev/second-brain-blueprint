---
type: system
---

# Optional policies

Policies that are **off by default**. Each one trades privacy or brevity
for completeness, and only the owner can decide whether that trade is
worth it for their life. None of them applies until the owner activates it.

The defaults stay in force either way: record what matters, label
uncertainty, no profile building of third parties
([AGENTS.md](../AGENTS.md#privacy-and-security),
[knowledge integrity](../.claude/rules/knowledge-integrity.md)). Two of the
defaults matter most when reading documents, and they apply to every
policy below:

- **Uncertain readings stay uncertain.** Record what a document says plus
  the doubt, never the likelier guess.
- **Never trust an OCR text layer for a value that matters.** Read names,
  numbers, amounts, dates and signatures off the image.

## How to activate a policy

1. Copy the policy text (the "Rule" block) into a rule file, for example
   `.claude/rules/medical-records.md`. Add `paths:` frontmatter if it only
   matters for certain folders, for example `04-areas/health/**`. For
   agents other than Claude Code, add the text to AGENTS.md instead (a
   short section under "Privacy and security").
2. Record the choice as a decision in `07-decisions/`, with the reason.
   Why: a later session that finds a file full of lab values or names
   should know this was deliberate, not a privacy slip.
3. Adapt the wording to your own situation. These are examples, not a
   standard.

To deactivate, delete the rule, mark the decision `superseded`, and leave
existing files as they are (they are history).

## Record medical documents in full

**Why someone would want it:** a lab value that is normal today is the
baseline for a comparison years from now. A summary ("blood work fine")
throws away exactly what a later doctor, or a later pattern check, needs.

**Rule:**

> Medical documents are recorded in full: every measured value with unit
> and reference range, including the unremarkable ones; every doctor,
> practice and laboratory with its identifiers; every date; the verbatim
> wording of medical instructions. Note empty fields as empty where that
> means something. Mark the file `sensitivity: confidential` and keep the
> scans out of the repository. Check poorly legible values visually: a
> guessed lab value is more dangerous than a missing one. Recording is not
> interpreting: name possible connections only as a labeled AI suggestion,
> never as an assessment.

## Record legal matters in full

**Why someone would want it:** in a legal proceeding the details are the
substance. A file number, a deadline or the exact wording of a claim that
was summarized away cannot be reconstructed when it is needed.

**Rule:**

> Legal matters are recorded in full: every name (parties, witnesses,
> lawyers, judges, case workers), every file number, deadline, hearing
> date, amount and claim, plus the alleged facts including quotes, also
> when a proceeding was discontinued. Mark the file
> `sensitivity: restricted` (or at least `confidential`) and keep the scans
> out of the repository. Do not summarize the identifiers away. Full
> recording is not permission to share: the restraint on passing content to
> third parties or external services stays.

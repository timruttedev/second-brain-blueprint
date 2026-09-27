# Taxonomy

The information types this system distinguishes and the minimal metadata
schema.

**This taxonomy is explicitly evolvable.** Agents may add, merge or remove
types when real usage justifies it. Every relevant change is reasoned and
logged in [organization-log.md](./learning/organization-log.md).

## Information types (v1)

| type | Meaning | Typical home |
|---|---|---|
| `capture` | Raw, untriaged input | `01-inbox/` |
| `journal` | Time-based note (what happened) | `02-journal/daily/` |
| `review` | Weekly, monthly or yearly synthesis | `02-journal/{weekly,monthly,yearly}/` |
| `project` | Time-bounded effort with an outcome | `03-projects/` |
| `area` | Ongoing responsibility, no end date | `04-areas/` |
| `person` | A person and their relation to the owner's life | `05-people/` |
| `knowledge` | Durable content that is looked up rather than acted on | `06-knowledge/` when it stands on its own; inside the owning area when it only makes sense there |
| `decision` | A durable decision record | `07-decisions/` |
| `goal` | An outcome the owner wants | inside the owning area or project; listed in [indexes/goals.md](./indexes/goals.md) |
| `resource` | External reference material | `08-resources/` |
| `system` | Part of the operating system itself | `00-system/` |

## Epistemic labels

Used inline (not in frontmatter) whenever the origin of a claim matters:

`confirmed fact` · `user statement` · `decision` · `assumption` ·
`hypothesis` · `AI suggestion` · `idea` · `external information`

Rule: AI-generated suggestions must never silently become personal facts.
When in doubt, label.

## Frontmatter schema (v1)

Use YAML frontmatter **sparingly**, only where it buys retrieval,
automation or organization. Base schema:

```yaml
---
type:        # one type from the table above
status:      # only where a lifecycle exists, see vocabularies below
created:     # YYYY-MM-DD
updated:     # YYYY-MM-DD (touch on meaningful edits)
scope:       # optional: area or topic this belongs to, e.g. "finances"
sensitivity: # only when NOT the default: public | confidential | restricted
max_lines:   # optional: the file's own line budget, checked by linkcheck.py
---
```

Rules:

- **Not every file needs every field.** A daily journal note needs none
  beyond what the file name says. A project file benefits from `type`,
  `status` and `updated`.
- **Default sensitivity is `private`.** Mark only exceptions. Rule of thumb:
  `confidential` for personal data and identifiers, `restricted` where
  disclosure could do concrete harm. See
  [privacy and security](../.claude/rules/privacy-security.md).
- **`type:` takes a value from the table above, nothing else.** A satellite
  file (a dated side file of a person or area) carries the same type as its
  canonical file. That it is a satellite shows in its name. A new type needs
  a stated retrieval benefit, a row in the table, and an update to the type
  list in [linkcheck.py](./scripts/linkcheck.py). Why: invented values
  spread quickly, get applied inconsistently, and nothing retrieves by them.
  The checker makes adding a type a deliberate act.
- **New fields only with a concrete, stated benefit.** Fields that go
  unused get removed again (log it). Why: a sentence alone does not stop
  new fields; the link checker reports every frontmatter key that is
  neither in the base schema nor in the domain fields below.
- **`max_lines:` is the file's own budget.** Use it only where brevity is
  the point, for example [current-context.md](./current-context.md), the
  entry point of every session. The link checker reports every file above
  its own value. Why: a budget written as a sentence gets exceeded by
  sessions that read the sentence.
- **Current means dated, not flagged.** No `status: current`. Freshness is
  carried by `updated:` and dated history lines
  ([temporal information](../.claude/rules/temporal-information.md)).

### Status vocabularies

`status:` has one vocabulary per lifecycle, not one shared list. Valid is
the union of these:

| For | Values |
|---|---|
| Base (projects, areas, archive) | `active` · `paused` · `done` · `archived` · `superseded` |
| Decisions | `proposed` · `accepted` · `superseded` · `reverted` |

A new lifecycle (for example drafts that get published) may add its own
vocabulary. Add it to this table and document it in the folder where it
applies.

### Domain fields

Besides the base schema, some file families may carry a documented extra
field. It needs a row here and an entry in the field list of
[linkcheck.py](./scripts/linkcheck.py):

| Field | On | Benefit |
|---|---|---|
| `archived:` | archived files | `YYYY-MM-DD`: says **when** it was archived, which `status: archived` does not ([archive workflow](./workflows/archive.md)) |
| `source:` | captures written by automation | Names the pipeline (e.g. `mail`, `documents`). Together with a source ID in the file name, it lets the next run recognize its own capture instead of writing a duplicate |

Keep a domain field only if it carries information that is not already in
the path or file name.

## Raw data exports

Besides the information types, **machine-generated raw material** (a CSV
export and the like) may live in the repository. Conditions: never edited
by hand, not canonical (the knowledge lives in the Markdown next to it),
and explained by a Markdown file.

How to handle the **next** export depends on the source. Check this once
when connecting a new source:

- **Full export** (the source delivers everything each time): **replace**
  the export. The Git diff is the change list.
- **Sliding window** (the source delivers only the last n months):
  **accumulate** exports, one file per export, never overwritten. Rebuild
  any derived total file from all exports. Why: replacing would delete
  history the source no longer returns.

## Generated evaluations

Generated Markdown (standard views of a data layer, so a recurring question
needs no script run) may live next to raw data. Four conditions, or it
turns into a number that is no longer true:

1. **A pure function of the source:** no run timestamp, no locale, no random
   order. Generating twice gives identical bytes.
2. **Generated automatically** on every run that touches the source data,
   never on request only.
3. **Data state in the file header** (scope, period, checksum of the
   source) plus a note that hand edits get lost.
4. **Checkable:** a command that exits non-zero when a file is missing,
   edited, or no longer matches the source.

Not canonical, like the raw material: the explaining Markdown is.

## Language

Agent instructions (AGENTS.md, CLAUDE.md, `.claude/rules/`, workflows,
templates) are English. Content files follow the owner's language. The
learning layer may quote the owner in their language: verbatim quotes are
evidence.

## File naming

- Lowercase, hyphen-separated, descriptive: `aws-cost-optimization.md`,
  `jane-doe.md`.
- Time-based files are date-prefixed: `2026-08-31.md`, `2026-W36.md`,
  `2026-08.md`, `2026.md`.
- Decisions: `YYYY-MM-DD-short-slug.md`.
- Inbox captures: timestamped atomic files, see
  [01-inbox/README.md](../01-inbox/README.md).

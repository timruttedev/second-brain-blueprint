# Workflow: Retrieval

Purpose: find an answer without loading the whole repository. The system
must still work with thousands of files and years of history, so retrieval
is hierarchical and search-first.

## Hierarchy

```
question
   ↓
00-system/current-context.md        (current focus, projects, loops)
   ↓
00-system/indexes/ + entity lookup  (which canonical file?)
   ↓
canonical file                      (the answer usually lives here)
   ↓
directly linked files               (only the ones the question needs)
   ↓
journal / history / archive         (only for questions about the past)
```

## Tactics

- **Search before reading**: `rg -il "term"` across likely directories;
  file name globs (`03-projects/*garden*`); follow links from indexes and
  canonical files. Frontmatter (`type:`, `scope:`, `status:`) is grep-able
  on purpose.
- Scope searches by the shape of the question:
  - who → `05-people/`
  - why → `07-decisions/`
  - when, what happened → `02-journal/`
  - how, what is → `06-knowledge/`
  - what to do → `03-projects/` and `04-areas/`
- Read sections, not whole large files, when the file has clear headings.
- `09-archive/` is excluded from default searches. Include it only when the
  question is explicitly historical or nothing current matches.
- Say where an answer came from (file path), and label it when it is an
  inference rather than a recorded fact.

## Learning signal

If something was hard to find (wrong guesses, repeated searches), that is an
observation for
[`observations.md`](../learning/observations.md). Repeated retrieval
failures are the main trigger for index and structure improvements.

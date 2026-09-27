---
name: brain-recall
description: Find information in the Second Brain, such as facts, project states, decisions and their reasons, people, and past events. Use when the user asks "what do I know about...", "why did I...", "when did...", "where is...", or any question the repository can answer.
---

# Brain Recall

Answer questions from the repository without loading all of it. Canonical
workflow: [retrieval.md](../../../00-system/workflows/retrieval.md). The
workflow doc wins on any conflict with this file.

Never load the whole repository. Go narrow to broad:

1. `00-system/current-context.md`
2. `00-system/indexes/`
3. the canonical file
4. directly linked files
5. journal and history, only for questions about the past

Search (`rg`, Glob) before reading content. Scope by the shape of the
question: who -> people, why -> decisions, when -> journal, how ->
knowledge, what to do -> projects, areas and `indexes/todos.md`. Leave
`09-archive/` out unless the question is historical.

Answer with the information AND its source file(s). Keep current state
apart from history, and owner statements apart from assumptions or AI
suggestions, as the files label them.

If retrieval was hard (wrong guesses, repeated searches), add a one-line
entry to `00-system/learning/observations.md`. That is how the structure
learns where it fails.

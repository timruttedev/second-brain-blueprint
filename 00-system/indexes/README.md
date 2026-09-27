# Indexes

Compact signposts for fast retrieval: **pointers, never content copies**.
One line per entry: name, one-phrase status or relevance, link. Each index
states its line format in its own header.

Maintained during triage and reviews. If an index stops improving retrieval,
remove it (and log the removal); if a new index would measurably help, add
it.

**Companion files hang off their owner's line.** When an entity grows a
companion file (for example a person's separate health or finance file), it
is not a new index entry. Append it to the owner's existing line as
`· [Label](link)`. A companion file carries the same `type:` as its
canonical file (see [taxonomy](../taxonomy.md)); that it is a companion
shows in its name. Why the rule is needed anyway: a pass that rebuilds the
index from canonical files ("one line per person or area") easily skips
the extra file, and then it becomes unreachable. Check by comparing the
files on disk against the index, not by memory.

Current indexes:

- [projects.md](./projects.md): active projects
- [areas.md](./areas.md): areas in active use
- [people.md](./people.md): currently relevant people
- [goals.md](./goals.md): current goals
- [decisions.md](./decisions.md): recent and high-impact decisions
- [todos.md](./todos.md): the one list of what the owner must do

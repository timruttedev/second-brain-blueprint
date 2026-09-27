# <OWNER_NAME>'s Second Brain

<!-- blueprint-only:start -->
<!-- This file becomes README.md when 00-system/scripts/init.py sets up a
     copy of the blueprint. Paths are written as code, not as links, because
     the file lives in 00-system/templates/ until then. -->
<!-- blueprint-only:end -->

My whole life's knowledge as plain Markdown files in Git: projects, areas,
people, decisions, knowledge and journal. AI agents capture, file, review
and maintain it; the files are the source of truth, not any chat or vendor
memory. **Private repository. Do not make it public.**

## How I use it

| I say | What happens |
|---|---|
| *"Note that ..."* | A capture lands in `01-inbox/` |
| *"triage"* | The inbox is filed into its canonical homes |
| *"What do I know about ...?"* / *"Why did I ...?"* | The agent answers from the files |
| *"I decided to ..."* | A decision record in `07-decisions/` |
| *"daily"*, *"weekly review"*, *"monthly review"* | Journal notes and reviews |
| *"Check the brain"* | Health check of the system itself |

Where to look first:

- `00-system/current-context.md`: what matters right now.
- `00-system/indexes/`: projects, areas, people, goals, decisions, to-dos.
- `AGENTS.md`: the operating manual every agent reads first. Change the
  rules there.

Before committing by hand, run the check:

```bash
python3 00-system/scripts/linkcheck.py --orphans
```

`GETTING-STARTED.md` covers the daily habits, the operating modes and the
optional scheduled routines.

## Upgrading

The system parts (`00-system/` without my own indexes, context and logs,
plus `.claude/`) come from the blueprint and can be updated from there. Read
its changelog, then follow
[Upgrading your copy](https://github.com/timruttedev/second-brain-blueprint#upgrading-your-copy).

## Credits

Built from [second-brain-blueprint](https://github.com/timruttedev/second-brain-blueprint)
by Tim Rutte, released under the MIT license.

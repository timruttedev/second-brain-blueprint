# Optimization Backlog

Improvement ideas deliberately **not** implemented yet. This keeps every
spontaneous idea from changing the architecture right away. Reviewed at the
monthly review; pick at most 1 or 2 items when the evidence supports them.

Suitable entries: new index strategies, automations, candidate metadata
fields, better review structures, retrieval improvements, possible
consolidations.

## Format

```
- [ ] YYYY-MM-DD: idea (evidence so far). Do when: <condition>
```

- Every idea names its **trigger** ("Do when"). An idea without a trigger
  is either done now or never.
- When an item is done, tick it and say where it went (organization-log
  entry, file, script). When it is discarded, strike it and say why.

## Backlog

Starter ideas (examples you may keep, change or delete):

- [ ] Automate daily note creation (a script or skill that stamps today's
  daily from the template). Do when: dailies are used regularly and creating
  them by hand is felt as friction.
- [ ] Per-year subfolders in `02-journal/daily/` (`daily/2031/...`). Do
  when: one directory holds more than about a year of dailies and listings
  become noisy.
- [ ] Split `type: knowledge` into finer types (for example a log type for
  time series). Do when: a retrieval visibly fails because `knowledge` is
  too broad, or one kind grows beyond a handful of files. Until then one
  type with a clear meaning is cheaper than three nobody tells apart.

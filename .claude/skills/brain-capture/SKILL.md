---
name: brain-capture
description: Capture a thought, idea, task, or piece of information into the Second Brain inbox with zero friction. Use when the user wants to quickly note something down, says "capture", "note this", "remember this", "write this down" (or the same in their own language), or shares information worth keeping without saying where it belongs.
---

# Brain Capture

Quick capture into `01-inbox/`. Canonical workflow:
[capture.md](../../../00-system/workflows/capture.md). The workflow doc wins
on any conflict with this file.

1. Take the user's content as it is. Do NOT ask about folders, tags or
   categories. Filing is triage's job.
2. Write one atomic file: `01-inbox/YYYY-MM-DD-HHMM-short-slug.md`
   (timestamp = now, slug = 2 to 5 words from the content). Content verbatim
   or lightly cleaned, in the user's language. Add `source:` or
   `relates to:` lines only when they are obvious from the conversation.
3. Exception: if the canonical home is unambiguous AND the edit is small
   (for example a new task for an existing project), file it directly there
   and say where it went.
4. Never capture secrets (passwords, keys, recovery codes). Strip them and
   say that you did.

Why one file per capture: two devices never edit the same file, so Git sync
never conflicts.

Confirm in one line what was captured and where.

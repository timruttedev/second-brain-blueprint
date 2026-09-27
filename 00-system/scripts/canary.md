# Canary for `linkcheck.py`

This file is broken on purpose. Do not fix it.

It contains exactly one link whose target does not exist:
[this target does not exist on purpose](./this-target-does-not-exist-on-purpose.md).
Every full run of [`linkcheck.py`](./linkcheck.py) **must** find it. If a
run does not find it, the script aborts with exit 2 instead of reporting
"0 findings". The finding then reads: the check is broken, not the
repository.

So that a normal run still stays green, `split_canary()` removes exactly
this one expected finding again. Any **other** finding in this file is
reported as usual.

## Why this exists

A check can stop checking and keep reporting success. That is worse than
having no check: without one you look yourself; with a green report you
stop looking
([Pattern](../learning/patterns.md#a-check-that-silently-reports-green-is-worse-than-none)).

## What this canary cannot do

It proves that checking and reporting still happen at all. It does not
catch one file whose rest is hidden behind a code fence that never closes,
because the machinery still runs in that case. The second check,
`open_fences()`, covers that: it reports every file that ends inside a code
block. Together they cover the two failure modes that actually occur, not
every possible one.

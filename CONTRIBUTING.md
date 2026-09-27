# Contributing

Thanks for helping to improve the blueprint. It is a personal system made
public, so changes are judged by one question: does this make a real
Second Brain work better in daily use?

## Ways to contribute

- **Report a bug:** a broken link, a check that misses something, a
  workflow that contradicts another. Use the bug template.
- **Propose an idea:** a better workflow, a new check, a lesson from your
  own Second Brain. Use the idea template, and say what problem you ran
  into; ideas backed by real use weigh more than ideas on paper.
- **Send a pull request:** for anything bigger than a typo, open an issue
  first so we can agree on the direction.

## Before you open a pull request

Run both checks from the repository root; both must pass:

```bash
python3 00-system/scripts/linkcheck.py --orphans
python3 -m unittest discover -s 00-system/scripts -t 00-system/scripts
```

And check your diff for long dashes, which the style rules forbid:

```bash
LC_ALL=C.UTF-8 git diff main | grep "^+" | LC_ALL=C.UTF-8 grep -P "[\x{2014}\x{2013}]"
```

The pull request template has the full checklist.

## Style rules

- **English** for everything in the repository: instructions, docs,
  examples, comments, commit messages.
- **Plain language.** Short sentences, concrete words, a reason next to
  every rule.
- **No em or en dashes** used as dashes. Use a colon, a comma,
  parentheses, or two sentences. Hyphens in compounds are fine.
- **No personal data.** Not yours, not anyone else's. Examples use the
  fictional persona in `examples/` or obvious placeholders.
- **Relative links that resolve**, with GitHub anchor slugs. The link
  checker enforces this.
- **A rule comes with its check** where it can. If you add a convention
  that a script could verify, extend `linkcheck.py` and its tests.
- **Commit messages** in English, imperative mood, saying what and why:
  `Check anchors in index files` rather than `fix`.
- Keep the [changelog](CHANGELOG.md) current: add a line under
  "Unreleased" for every change a user would notice.

## License

By contributing you agree that your contribution is released under the
[MIT license](LICENSE) of this repository.

#!/usr/bin/env python3
"""Turn a fresh copy of the blueprint into your own Second Brain.

    python3 00-system/scripts/init.py --name "Alex Morgan" --language English \\
        --timezone Europe/Berlin [--keep-examples] [--dry-run] [--force]

What it does, in this order:

1. Replaces the placeholders `<OWNER_NAME>`, `<OWNER_LANGUAGE>` and
   `<TIMEZONE>` in every text file, except GETTING-STARTED.md (which
   explains them) and this script and its test.
2. Replaces `updated: YYYY-MM-DD` and `created: YYYY-MM-DD` with today's
   date, but only in 00-system/current-context.md and
   00-system/indexes/*.md. Everywhere else `YYYY-MM-DD` is a format
   example and must stay.
3. Removes every block between `<!-- blueprint-only:start -->` and
   `<!-- blueprint-only:end -->` (markers included) in any .md file. The
   markers count only on a line of their own and outside code fences.
4. Replaces README.md with 00-system/templates/README.owner.md.
5. Deletes what only the blueprint project needs: examples/ (unless
   --keep-examples), CHANGELOG.md, CONTRIBUTING.md, SECURITY.md,
   CODE_OF_CONDUCT.md, .github/ISSUE_TEMPLATE/ and
   .github/PULL_REQUEST_TEMPLATE.md. The CI workflow
   .github/workflows/checks.yml stays.
6. Runs linkcheck.py and prints the next steps.

Idempotent: a second run finds no placeholders and refuses, unless --force
is given. --dry-run lists every change and writes nothing. Git is the undo:
run it on a clean working tree and review `git diff` before committing.

Standard library only, Python 3.10 or newer.
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

PLACEHOLDERS = ("<OWNER_NAME>", "<OWNER_LANGUAGE>", "<TIMEZONE>")
# Files that talk *about* the placeholders and must keep them.
NO_REPLACE = {
    "GETTING-STARTED.md",
    "00-system/scripts/init.py",
    "00-system/scripts/test_init.py",
}
SKIP_PARTS = {".git", "__pycache__", "node_modules", "worktrees"}

DATE_FILES = ("00-system/current-context.md", "00-system/indexes/")
_DATE_FIELD = re.compile(r"^(updated|created):[ \t]*YYYY-MM-DD[ \t]*$", re.MULTILINE)

START = "<!-- blueprint-only:start -->"
END = "<!-- blueprint-only:end -->"
_FENCE = re.compile(r"^\s*(`{3,}|~{3,})")

OWNER_README = "00-system/templates/README.owner.md"
BLUEPRINT_FILES = (
    "CHANGELOG.md", "CONTRIBUTING.md", "SECURITY.md", "CODE_OF_CONDUCT.md",
    ".github/ISSUE_TEMPLATE", ".github/PULL_REQUEST_TEMPLATE.md",
)
EXAMPLES = "examples"


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def text_files() -> list[Path]:
    """Every UTF-8 text file in the repository, skipping Git and caches."""
    result = []
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path.is_symlink():
            continue
        if any(part in SKIP_PARTS for part in path.relative_to(ROOT).parts):
            continue
        try:
            path.read_bytes().decode("utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        result.append(path)
    return result


def placeholders_left(files: list[Path]) -> int:
    count = 0
    for path in files:
        if rel(path) in NO_REPLACE:
            continue
        text = path.read_text(encoding="utf-8")
        count += sum(text.count(p) for p in PLACEHOLDERS)
    return count


def strip_blueprint_only(text: str) -> tuple[str, int, bool]:
    """(text without blueprint-only blocks, blocks removed, unclosed?)"""
    out, removed = [], 0
    in_fence, in_block = False, False
    for line in text.splitlines(keepends=True):
        stripped = line.strip()
        if not in_block and _FENCE.match(line):
            in_fence = not in_fence
        if not in_fence and stripped == START and not in_block:
            in_block = True
            continue
        if in_block:
            if stripped == END:
                in_block = False
                removed += 1
            continue
        out.append(line)
    if in_block:
        # An unclosed block is left untouched: better visible than lost.
        return text, 0, True
    return "".join(out), removed, False


def today_in(zone: str) -> dt.date:
    try:
        from zoneinfo import ZoneInfo
        return dt.datetime.now(ZoneInfo(zone)).date()
    except Exception:  # unknown zone or no tz database: local date
        return dt.date.today()


def valid_zone(zone: str) -> bool:
    try:
        from zoneinfo import ZoneInfo
        ZoneInfo(zone)
        return True
    except Exception:
        return False


def plan(args: argparse.Namespace) -> list[tuple[str, str, object]]:
    """[(action, path, payload)]: everything init would do, nothing done yet."""
    actions: list[tuple[str, str, object]] = []
    values = {
        "<OWNER_NAME>": args.name,
        "<OWNER_LANGUAGE>": args.language,
        "<TIMEZONE>": args.timezone,
    }
    today = today_in(args.timezone).isoformat()
    deleted = [ROOT / p for p in BLUEPRINT_FILES]
    if not args.keep_examples:
        deleted.append(ROOT / EXAMPLES)

    def doomed(path: Path) -> bool:
        return any(path == d or d in path.parents for d in deleted)

    owner_readme = ROOT / OWNER_README
    for path in text_files():
        if doomed(path):
            continue
        name = rel(path)
        if name == "README.md" and owner_readme.is_file():
            continue  # replaced as a whole below
        original = path.read_text(encoding="utf-8")
        text = original
        notes = []
        if name not in NO_REPLACE:
            n = sum(text.count(p) for p in PLACEHOLDERS)
            for key, value in values.items():
                text = text.replace(key, value)
            if n:
                notes.append(f"{n} placeholder(s)")
        if name.startswith(DATE_FILES) and name.endswith(".md"):
            text, n = _DATE_FIELD.subn(lambda m: f"{m.group(1)}: {today}", text)
            if n:
                notes.append(f"{n} date field(s)")
        if path.suffix == ".md":
            text, n, unclosed = strip_blueprint_only(text)
            if n:
                notes.append(f"{n} blueprint-only block(s)")
            if unclosed:
                print(f"Warning: {name}: blueprint-only block never closed, "
                      f"left as it is.", file=sys.stderr)
        if text != original:
            actions.append(("write", name, (text, ", ".join(notes))))

    if owner_readme.is_file():
        text = owner_readme.read_text(encoding="utf-8")
        for key, value in values.items():
            text = text.replace(key, value)
        text, _, _ = strip_blueprint_only(text)
        readme = ROOT / "README.md"
        current = readme.read_text(encoding="utf-8") if readme.is_file() else None
        if text != current:
            actions.append(("write", "README.md", (text, f"from {OWNER_README}")))
    else:
        print(f"Warning: {OWNER_README} is missing, README.md stays as it is.",
              file=sys.stderr)

    for path in deleted:
        if path.exists():
            actions.append(("delete", rel(path), None))
    return actions


def apply(actions: list[tuple[str, str, object]]) -> None:
    for action, name, payload in actions:
        path = ROOT / name
        if action == "write":
            text, _ = payload
            path.write_text(text, encoding="utf-8")
        elif action == "delete":
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()


def linkcheck() -> int:
    script = ROOT / "00-system" / "scripts" / "linkcheck.py"
    if not script.is_file():
        print("linkcheck.py not found, skipped.")
        return 0
    print("\nRunning linkcheck.py ...")
    return subprocess.run([sys.executable, str(script)], cwd=ROOT).returncode


NEXT_STEPS = """
Next steps:
  1. Review the changes:       git status && git diff
  2. Commit them:              git add -A && git commit -m "Initialize Second Brain"
  3. Fill in 00-system/current-context.md (who you are, current focus).
  4. Start your agent in this folder and capture your first thought.
  See GETTING-STARTED.md for the full walkthrough.
"""


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--name", required=True, help="your name, as agents should use it")
    p.add_argument("--language", required=True,
                   help="the language agents talk to you in, e.g. English")
    p.add_argument("--timezone", required=True,
                   help="IANA time zone, e.g. Europe/Berlin or America/New_York")
    p.add_argument("--keep-examples", action="store_true",
                   help="keep the fictional sample Second Brain in examples/")
    p.add_argument("--dry-run", action="store_true",
                   help="list what would change, write nothing")
    p.add_argument("--force", action="store_true",
                   help="run even if no placeholders are left or the time "
                        "zone is unknown")
    args = p.parse_args(argv)

    for label, value in (("--name", args.name), ("--language", args.language),
                         ("--timezone", args.timezone)):
        if not value.strip() or any(ch in value for ch in "\n\r<>"):
            print(f"{label} must be a non-empty single line without < or >.",
                  file=sys.stderr)
            return 2
    if not valid_zone(args.timezone) and not args.force:
        print(f"Unknown time zone {args.timezone!r}. Use an IANA name such as "
              f"Europe/Berlin (or --force if your system has no time zone "
              f"database).", file=sys.stderr)
        return 2

    if not placeholders_left(text_files()) and not args.force:
        print("No placeholders left: this Second Brain looks initialized "
              "already. Nothing done (use --force to run anyway).")
        return 1

    actions = plan(args)
    for action, name, payload in actions:
        if action == "write":
            print(f"{'would update' if args.dry_run else 'updated'}  {name}"
                  f"  ({payload[1]})")
        else:
            print(f"{'would delete' if args.dry_run else 'deleted'}  {name}")
    if not actions:
        print("Nothing to change.")
    if args.dry_run:
        print("\nDry run: nothing was written.")
        return 0

    apply(actions)
    code = linkcheck()
    if code:
        print("\nlinkcheck.py reported findings (see above). Fix them before "
              "the first commit.")
    print(NEXT_STEPS)
    return 1 if code else 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Check internal links, anchors, orphans, frontmatter and line budgets.

How and when to run it: 00-system/workflows/system-health-check.md

    linkcheck.py                     # every .md file in the repository
    linkcheck.py <path> ...          # only these files
    linkcheck.py --orphans           # also report files nobody mentions
    linkcheck.py --only-orphans

Exit 1 as soon as a link, an anchor, a `type:`, a `status:`, a
`sensitivity:` or a frontmatter field does not resolve, a file exceeds its
own `max_lines`, a code fence is never closed, a learning-log signpost
carries a dated entry (entries belong in the month files), or an
evaluation in the organization log is due. Orphans are a hint, not an
error. Exit 2 when the canary is silent:
then the check itself is broken, not the repository.

Why a script: a renamed heading silently breaks anchor links, and manual
checks drown in format placeholders ("just an example, not a link"). This
script sorts those out instead of reporting them: text inside a code
block, inline code or an HTML comment does not count as a link. For
*anchors*, inline code does count, because a heading may contain a code
word.

Why `type:`, `status:` and field names: the taxonomy allows only the values
in its tables (00-system/taxonomy.md). Agents invent new values anyway, even
when they know the rule. A rule nobody can check gets broken again, and a
cleanup alone only produces the next round.

The anchor rule follows GitHub: lowercase, drop Markdown markup and special
characters, turn **every** whitespace character into a hyphen. Do not
collapse them: 'Step 1 ⚠️ Setup' becomes 'step-1--setup', with two hyphens,
because the emoji vanishes between two spaces. Collapsing would report
every emoji anchor as broken.

`examples/` (the fictional sample Second Brain) is checked for links,
anchors and frontmatter like everything else, but it is left out of the
orphan check and of the due-evaluation check: its files are reached through
the examples README, and its dates are fixed sample dates, not deadlines.
Pass an example log file explicitly to check its evaluations anyway.
"""

import argparse
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# Orphans are normal here and are not reported: directory READMEs (reached
# through the folder), the journal (reached by date), the inbox (transit),
# the archive, the agent instructions at the root, everything under
# .claude/ (the runtime reads those, not a link) and .github/.
ORPHAN_EXEMPT_PREFIXES = ("02-journal/", "01-inbox/", ".claude/", "09-archive/",
                          ".github/")
ORPHAN_EXEMPT_NAMES = {"README.md", "AGENTS.md", "CLAUDE.md"}
# The fictional sample Second Brain. Its links are checked, but it takes no
# part in the orphan check (neither as orphan nor as the file that mentions
# one) and its organization log is not evaluated unless passed explicitly.
EXAMPLES = "examples/"

_FENCE = re.compile(r"^\s*(`{3,}|~{3,})(.*)$")
_COMMENT_OPEN = re.compile(r"<!--")
_COMMENT_CLOSE = re.compile(r"-->")
_INLINE_CODE = re.compile(r"`[^`\n]*`")
_LINK = re.compile(r"(?<!!)\[[^\]]*\]\(\s*([^)\s]+)")
_MD_LINK_TEXT = re.compile(r"\[([^\]]*)\]\([^)]*\)")
# The underscore stays: GitHub keeps it inside a word. '`max_lines` field'
# becomes 'max_lines-field'; dropping it as markup would break every such
# anchor.
_MARKUP = re.compile(r"[*`~]")
_NOT_SLUG = re.compile(r"[^\w\s-]", re.UNICODE)
_EXTERNAL = ("http://", "https://", "mailto:", "tel:", "ftp://")

# The eleven values from the type table in 00-system/taxonomy.md. A new value
# goes into that table first (with a stated retrieval benefit) and then
# here, never the other way round.
TYPES = {
    "capture", "journal", "review", "project", "area", "person",
    "knowledge", "decision", "goal", "resource", "system",
}
# The taxonomy itself shows the field as a schema placeholder.
TYPE_EXEMPT = {"00-system/taxonomy.md"}
# `[ \t]*`, not `\s*`: an empty `type:` must not swallow the next line's key.
_TYPE = re.compile(r"^type:[ \t]*([^\s#]+)", re.MULTILINE)
_MAX_LINES = re.compile(r"^max_lines:\s*(\d+)\s*$", re.MULTILINE)

# The union of the documented status vocabularies in 00-system/taxonomy.md.
# **Deliberately a union, not one list per type:** a check against a single
# vocabulary would flag `accepted` on decisions although it is documented,
# and a check per type would need a file-to-lifecycle mapping that does not
# exist. The union catches what it should: a value nobody decided on.
STATUSES = {
    "active", "paused", "done", "archived", "superseded",   # base
    "proposed", "accepted", "reverted",                     # decisions
}
# Base schema plus documented extra fields, also from the taxonomy. A new
# field goes into the taxonomy first (with a named benefit) and then here.
FIELDS = {
    "type", "status", "created", "updated", "scope", "sensitivity",
    "max_lines", "archived", "source",
}
# Frontmatter under .claude/ and .github/ belongs to the tools, not the
# taxonomy: skills carry name/description, rules carry paths, issue
# templates carry name/about/labels. Exempt from type, status and field
# checks alike.
FIELD_EXEMPT_PREFIXES = (".claude/", ".github/")
_STATUS = re.compile(r"^status:[ \t]*([^\s#]+)", re.MULTILINE)
# The four sensitivity levels from 00-system/taxonomy.md. `private` is the
# default and normally not written, but it is not wrong either.
SENSITIVITIES = {"public", "private", "confidential", "restricted"}
_SENSITIVITY = re.compile(r"^sensitivity:[ \t]*([^\s#]+)", re.MULTILINE)
_KEY = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*):", re.MULTILINE)

# Organization log: an open evaluation names a review date.
# Format: 00-system/learning/organization-log.md.
ORGLOG = "00-system/learning/organization-log/"
_ENTRY = re.compile(r"^##\s+(\d{4})-(\d{2})-(\d{2})\b")
_RESULT = re.compile(r"^Result:\s*(.*)$")
_FIELD_LINE = re.compile(r"^[A-Za-z][A-Za-z]*:\s")
_DATE_ISO = re.compile(r"\b(\d{4})-(\d{2})-(\d{2})\b")
# Open stays open in any spelling: '_open', 'open,', '_open_', '_pending'.
_OPEN = ("open", "pending")
# Days an entry without a review date gets before it becomes a finding. One
# month, because the monthly review is what closes it.
GRACE_DAYS = 30

# The two learning-log signposts hold the format and the month table only.
# Entries go into the month files next to them (00-system/learning/README.md).
SIGNPOSTS = (
    "00-system/learning/organization-log.md",
    "00-system/learning/observations.md",
)
# An organization-log entry starts with a dated heading, an observation with
# a dated bullet. Inside a code fence (the documented format) neither counts.
_DATED_ENTRY = re.compile(r"^(?:#{1,6}\s+|[-*]\s+)\d{4}-\d{2}-\d{2}\b")


def is_fence(line):
    """Does this line open or close a code block?

    Per CommonMark, the info string of a ``` fence must **not** contain
    another backtick; otherwise the line is prose, and GitHub renders it as
    prose. A naive rule ('line starts with three backticks') treats such a
    prose line as a fence that never closes and silently skips the rest of
    the file while still reporting zero findings.
    """
    match = _FENCE.match(line)
    if not match:
        return False
    mark, rest = match.group(1), match.group(2)
    return not (mark.startswith("`") and "`" in rest)


def strip_code(text, inline=True):
    """Blank out code blocks, HTML comments and (optionally) inline code.

    Replaces them character by character with spaces instead of removing
    them, so line numbers and columns of the remaining matches stay right.

    `inline=False` for headings: a code word in a heading is part of the
    anchor. Blanking it would drop exactly the word that carries the anchor.
    """
    lines = []
    in_block = False
    in_comment = False
    for line in text.split("\n"):
        if is_fence(line):
            in_block = not in_block
            lines.append("")
            continue
        if in_block:
            lines.append("")
            continue
        rest = line
        if in_comment:
            end = _COMMENT_CLOSE.search(rest)
            if not end:
                lines.append("")
                continue
            rest = " " * end.end() + rest[end.end():]
            in_comment = False
        while True:
            opening = _COMMENT_OPEN.search(rest)
            if not opening:
                break
            closing = _COMMENT_CLOSE.search(rest, opening.end())
            if not closing:
                rest = rest[:opening.start()] + " " * (len(rest) - opening.start())
                in_comment = True
                break
            rest = (rest[:opening.start()]
                    + " " * (closing.end() - opening.start())
                    + rest[closing.end():])
        if inline:
            rest = _INLINE_CODE.sub(lambda m: " " * len(m.group(0)), rest)
        lines.append(rest)
    return "\n".join(lines)


def slug(heading):
    """Heading text -> anchor, following GitHub's rule."""
    s = heading.lstrip("#").strip()
    s = _MD_LINK_TEXT.sub(r"\1", s)          # [text](target) -> text
    s = _MARKUP.sub("", s).lower()
    s = _NOT_SLUG.sub("", s)
    return re.sub(r"\s", "-", s)


def anchors(text):
    """All anchors of a file, including the -1/-2 suffixes for duplicates."""
    seen, result = {}, set()
    for line in strip_code(text, inline=False).split("\n"):
        if not line.startswith("#"):
            continue
        s = slug(line)
        if not s:
            continue
        n = seen.get(s, 0)
        seen[s] = n + 1
        result.add(s if n == 0 else f"{s}-{n}")
    return result


def links(text):
    """(line number, target) for each internal link, ignoring code and comments."""
    for no, line in enumerate(strip_code(text).split("\n"), start=1):
        for match in _LINK.finditer(line):
            target = match.group(1).strip("<>")
            if target.lower().startswith(_EXTERNAL):
                continue
            yield no, target


def check(files):
    """[(file, line, target, kind)] with kind 'missing' or 'anchor'."""
    anchor_cache = {}
    findings = []
    for path in files:
        text = path.read_text(encoding="utf-8")
        for no, target in links(text):
            rel, _, mark = target.partition("#")
            mark = mark.lower()
            target_file = path if not rel else (path.parent / rel)
            if rel:
                try:
                    target_file = target_file.resolve(strict=True)
                except (OSError, RuntimeError):
                    findings.append((path, no, target, "missing"))
                    continue
            if not mark or target_file.suffix != ".md" or target_file.is_dir():
                continue
            if target_file not in anchor_cache:
                anchor_cache[target_file] = anchors(
                    target_file.read_text(encoding="utf-8"))
            if mark not in anchor_cache[target_file]:
                findings.append((path, no, target, "anchor"))
    return findings


def orphans(files):
    """Files that no other Markdown file mentions.

    Mentioned means: as a Markdown link **or** as a path in the text.
    Workflows and templates are usually named as a path
    ('`00-system/templates/project.md`'), not linked. Counting only links
    would turn them all into orphans, and the report would be noise.
    """
    files = [p for p in files if not relative(p).startswith(EXAMPLES)]
    linked = set()
    texts = {}
    for path in files:
        texts[path] = path.read_text(encoding="utf-8")
        for _, target in links(texts[path]):
            rel = target.partition("#")[0]
            if not rel:
                continue
            try:
                linked.add((path.parent / rel).resolve(strict=True))
            except (OSError, RuntimeError):
                pass
    for path in files:
        if path.resolve() in linked:
            continue
        name = path.name
        rel = relative(path)
        if any(rel in text or name in text
               for other, text in texts.items() if other != path):
            linked.add(path.resolve())
    result = []
    for path in files:
        rel = relative(path)
        if path.name in ORPHAN_EXEMPT_NAMES:
            continue
        if rel.startswith(ORPHAN_EXEMPT_PREFIXES):
            continue
        if path.resolve() not in linked:
            result.append(path)
    return result


def relative(path):
    """Path from the root as a POSIX string, or absolute if outside the root.

    A file passed on the command line may lie outside the root; then no
    exemption applies, but the check must not crash.
    """
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()



def header(path):
    """The frontmatter of a file, or None.

    That is the block between the first two '---' lines. Anything further
    down belongs to a table or an example and does not describe the file.
    The taxonomy itself forces this: it shows every schema field as an
    example.
    """
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    return text[4:end]


def types(files):
    """[(file, line, value)] for each `type:` not in the taxonomy."""
    findings = []
    for path in files:
        rel = relative(path)
        if rel in TYPE_EXEMPT or rel.startswith(FIELD_EXEMPT_PREFIXES):
            continue
        head = header(path)
        if head is None:
            continue
        match = _TYPE.search(head)
        if match and match.group(1) not in TYPES:
            no = 2 + head[:match.start()].count("\n")
            findings.append((path, no, match.group(1)))
    return findings


def frontmatter(files):
    """[(file, line, kind, value)] for each unknown status, sensitivity or field.

    `kind` is "status", "sensitivity" or "field"; the caller words the
    message. Both come
    from one loop because they share a cause: a convention that lives only
    in the taxonomy does not hold.
    """
    findings = []
    for path in files:
        rel = relative(path)
        if any(rel.startswith(p) for p in FIELD_EXEMPT_PREFIXES):
            continue
        head = header(path)
        if head is None:
            continue
        match = _STATUS.search(head)
        if match and match.group(1) not in STATUSES:
            no = 2 + head[:match.start()].count("\n")
            findings.append((path, no, "status", match.group(1)))
        match = _SENSITIVITY.search(head)
        if match and match.group(1) not in SENSITIVITIES:
            no = 2 + head[:match.start()].count("\n")
            findings.append((path, no, "sensitivity", match.group(1)))
        for match in _KEY.finditer(head):
            if match.group(1) not in FIELDS:
                no = 2 + head[:match.start()].count("\n")
                findings.append((path, no, "field", match.group(1)))
    return findings


def line_budgets(files):
    """[(file, budget, actual)] for each file over its own `max_lines`.

    A file may declare its own line budget in its frontmatter; exceeding it
    is a finding. Only the frontmatter counts, for the same reason as in
    `types()`: a prose sentence must not commit a file to a rule.

    Why: a budget written as a sentence at the top of a file gets exceeded
    by sessions that read the sentence. Every session adds a clarification,
    none shortens. The budget lives **in** the file, not in a list here: a
    list of file names with numbers in this script would be a copy, and
    copies go stale.
    """
    findings = []
    for path in files:
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            continue
        end = text.find("\n---", 4)
        if end == -1:
            continue
        match = _MAX_LINES.search(text[4:end])
        if not match:
            continue
        budget = int(match.group(1))
        actual = len(text.rstrip("\n").split("\n"))
        if actual > budget:
            findings.append((path, budget, actual))
    return findings


#: The canary: a file with a deliberately broken link that every full run
#: **must** find. If it does not, the repository is not fine; the check is
#: broken, and the run aborts with exit 2 instead of reporting "0 findings".
#:
#: Honest about its reach: the canary proves that checking and reporting
#: still happen at all. It does not catch a single file whose rest is hidden
#: behind an unclosed fence; `open_fences()` covers that case.
CANARY = "00-system/scripts/canary.md"
CANARY_TARGET = "./this-target-does-not-exist-on-purpose.md"


def split_canary(findings, files):
    """(real findings, error text or None).

    Only meaningful on a full run: whoever passes single files does not
    check the canary and must not fail because of it.
    """
    path = (ROOT / CANARY).resolve()
    if path not in files:
        return findings, None
    expected = [f for f in findings if f[0] == path and f[2] == CANARY_TARGET]
    real = [f for f in findings if not (f[0] == path and f[2] == CANARY_TARGET)]
    if not expected:
        return real, (
            f"CANARY SILENT: the deliberately broken link {CANARY_TARGET!r} "
            f"in {CANARY} was not reported.\n"
            "This run is worthless: it can no longer show that it checks "
            "anything. Do not fix the repository, fix this script.")
    return real, None


def open_fences(files):
    """[(file, line)] for each file that ends inside a code block.

    A fence that never closes hides the rest of the file: links, anchors
    and headings after it are no longer checked, and the run still reports
    nothing. Usually the cause is not a real code block but a prose line
    that starts with three backticks.
    """
    findings = []
    for path in files:
        open_at = None
        for no, line in enumerate(path.read_text(encoding="utf-8").split("\n"),
                                  start=1):
            if is_fence(line):
                open_at = None if open_at else no
        if open_at:
            findings.append((path, open_at))
    return findings


def collect(paths):
    if paths:
        return sorted(Path(p).resolve() for p in paths)
    # Check relative parts, not absolute ones: when the script itself runs
    # inside a worktree under .claude/worktrees/, every absolute path
    # contains "worktrees" and the selection would be empty.
    skip = (".git", "worktrees", "node_modules", "__pycache__")
    return sorted(
        p.resolve() for p in ROOT.rglob("*.md")
        if not any(part in skip for part in p.relative_to(ROOT).parts)
    )


def signpost_entries(files):
    """[(file, line)] for each dated entry written into a signpost.

    `observations.md` and `organization-log.md` hold the format and the
    month table. An entry written there instead of into the month file is
    invisible to the due-evaluation check and makes the signpost grow
    until nobody reads it. The documented format sits in a code fence and
    does not count; neither does an HTML comment.
    """
    findings = []
    for path in files:
        rel = relative(path)
        if not any(rel == s or rel == EXAMPLES + s for s in SIGNPOSTS):
            continue
        text = strip_code(path.read_text(encoding="utf-8"), inline=False)
        for no, line in enumerate(text.split("\n"), start=1):
            if _DATED_ENTRY.match(line):
                findings.append((path, no))
    return findings


def _dates(text):
    """All ISO dates (YYYY-MM-DD) in the text."""
    found = []
    for year, month, day in _DATE_ISO.findall(text):
        try:
            found.append(date(int(year), int(month), int(day)))
        except ValueError:
            pass
    return found


def due_evaluations(files, today=None, include_examples=False):
    """[(file, line, reason, title)] for each overdue open evaluation.

    An organization-log entry carries a `Result:`. If it says `open` or
    `pending`, the change is not evaluated yet, and it stays that way if
    nobody follows up. A sentence in a workflow does not close anything;
    this check does.

    An open entry is due in two ways:

    1. Its **review date** has been reached. The review date is the latest
       date in the result block that lies **after the heading date**: a
       deadline is set in the future when writing, while a past date points
       to an incident and is not a deadline.
    2. It names **no such date** and is older than `GRACE_DAYS` (counted
       from the date in its heading). "Check at the next review" is not a
       deadline but the absence of one.

    Both are closed by the same move: write a verdict (keep / modify /
    revert) or set a concrete date.

    `examples/00-system/learning/organization-log/` only counts with
    `include_examples` (set when files are passed on the command line):
    sample dates would otherwise turn due and fail every run.
    """
    today = today or date.today()
    prefixes = (ORGLOG, EXAMPLES + ORGLOG) if include_examples else (ORGLOG,)
    findings = []
    for path in files:
        if not relative(path).startswith(prefixes):
            continue
        lines = path.read_text(encoding="utf-8").splitlines()
        title, posted = None, None
        no = 0
        while no < len(lines):
            line = lines[no]
            head = _ENTRY.match(line)
            if head:
                title = line.lstrip("#").strip()
                try:
                    posted = date(*(int(g) for g in head.groups()))
                except ValueError:
                    posted = None
                no += 1
                continue
            match = _RESULT.match(line)
            if not match:
                no += 1
                continue
            result_line = no + 1
            block = [match.group(1).strip()]
            no += 1
            while no < len(lines):
                following = lines[no]
                if (not following.strip() or following.startswith("#")
                        or following.startswith("---")
                        or _FIELD_LINE.match(following)):
                    break
                block.append(following.strip())
                no += 1
            text = " ".join(block).strip()
            if not text.strip(" _*").lower().startswith(_OPEN):
                continue
            # Only dates after the heading are deadlines, see docstring.
            deadlines = [d for d in _dates(text) if posted and d > posted]
            if deadlines:
                deadline = max(deadlines)
                if deadline <= today:
                    findings.append((path, result_line,
                                     f"review date {deadline.isoformat()} passed",
                                     title))
            elif posted and (today - posted).days >= GRACE_DAYS:
                findings.append((path, result_line,
                                 f"open for {(today - posted).days} days "
                                 f"without a review date", title))
    return findings


def main():
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    p.add_argument("paths", nargs="*", help="files to check (default: all)")
    p.add_argument("--orphans", action="store_true",
                   help="also report files nobody mentions")
    p.add_argument("--only-orphans", action="store_true")
    args = p.parse_args()

    files = collect(args.paths)
    findings = [] if args.only_orphans else check(files)
    if not args.only_orphans:
        findings, silent = split_canary(findings, files)
        if silent:
            print(silent, file=sys.stderr)
            return 2
    for path, no, target, kind in findings:
        word = "target missing" if kind == "missing" else "anchor missing"
        print(f"{relative(path)}:{no}: {word}: {target}")

    fence_findings = [] if args.only_orphans else open_fences(files)
    for path, no in fence_findings:
        print(f"{relative(path)}:{no}: code fence never closed, nothing after it "
              f"was checked")

    type_findings = [] if args.only_orphans else types(files)
    for path, no, value in type_findings:
        print(f"{relative(path)}:{no}: type not in the taxonomy: {value}")

    head_findings = [] if args.only_orphans else frontmatter(files)
    for path, no, kind, value in head_findings:
        what = {
            "status": "status not in a documented vocabulary",
            "sensitivity": "sensitivity not one of "
                           + "/".join(sorted(SENSITIVITIES)),
        }.get(kind, "frontmatter field not in the taxonomy")
        print(f"{relative(path)}:{no}: {what}: {value}")

    post_findings = [] if args.only_orphans else signpost_entries(files)
    for path, no in post_findings:
        print(f"{relative(path)}:{no}: dated entry in a signpost: entries "
              f"belong in the month files")

    eval_findings = ([] if args.only_orphans else
                     due_evaluations(files, include_examples=bool(args.paths)))
    for path, no, reason, title in eval_findings:
        short = title if len(title) <= 60 else title[:57] + "..."
        print(f"{relative(path)}:{no}: evaluation due ({reason}): {short}")

    budget_findings = [] if args.only_orphans else line_budgets(files)
    for path, budget, actual in budget_findings:
        print(f"{relative(path)}: {actual} lines, declared budget {budget} "
              f"(max_lines in frontmatter)")

    if args.orphans or args.only_orphans:
        # Only meaningful on a full run: when checking single files,
        # everything outside the selection looks unlinked.
        lonely = orphans(files)
        if args.paths:
            print("Note: --orphans only considers the files passed.")
        for path in lonely:
            print(f"{relative(path)}: not mentioned by any file")
        print(f"\n{len(lonely)} orphan(s) among {len(files)} files.")

    total = (len(findings) + len(fence_findings) + len(type_findings)
             + len(head_findings) + len(budget_findings) + len(eval_findings)
             + len(post_findings))
    print(f"{len(files)} files checked, {total} finding(s).")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())

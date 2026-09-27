#!/usr/bin/env python3
"""What lies on branches that `main` does not have yet.

A session that only reads the working tree cannot see work that is finished
but unmerged. In multi-session mode that blind spot is built in: a task
ends with a pull request and branches are pushed early. Without this check,
two sessions move the same capture to two different places, or build
against a decision that sits unmerged on another branch.

So: run this **before** triage, before creating a canonical file, and before
building a mechanism. It answers one question. *Has somebody already done
this, on a branch I am not standing on?*

Deliberately branch-based, not pull-request-based. Branches need no token and
no network service, they work in every checkout including scheduled cloud
runs, and a branch may carry work without any pull request at all. When `gh`
happens to be available and authenticated, the pull-request number and its
mergeability are added on top; without it the report is complete, just less
convenient.

It never reports "all clear" while it had to skip a branch. A shallow clone
(common in cloud checkouts) often lacks the common ancestor of a branch and
`main`; such a branch is counted and named, with a hint to deepen the clone.

Exit code is 0 unless --strict is given: this is a briefing, not a gate.

  python3 00-system/scripts/branch_overview.py
  python3 00-system/scripts/branch_overview.py --fetch      # fetch all branches first
  python3 00-system/scripts/branch_overview.py --paths      # every file, not just overlaps
  python3 00-system/scripts/branch_overview.py --strict     # exit 1 if anything is open
"""
from __future__ import annotations

import argparse
import collections
import datetime as dt
import json
import shutil
import subprocess
import sys

MAIN = "origin/main"
# A plain `git fetch` in a single-branch clone only updates main. This
# refspec brings every branch of the remote, which is the point here.
REFSPEC = "+refs/heads/*:refs/remotes/origin/*"
DEEPEN = 200
# Files almost every branch touches. Reporting them as collisions would bury
# the real ones, which is how a check stops being read.
NOISE = {
    "00-system/current-context.md",
    "00-system/learning/observations.md",
}
NOISE_PREFIX = (
    "00-system/learning/observations/",
    "00-system/learning/organization-log/",
)


def git(*args: str, cwd: str | None = None) -> str:
    """stdout of a git command, or "" when it fails."""
    r = subprocess.run(["git", *args], capture_output=True, timeout=300, cwd=cwd)
    if r.returncode != 0:
        return ""
    return r.stdout.decode("utf-8", "replace").strip()


def git_ok(*args: str, cwd: str | None = None) -> bool:
    r = subprocess.run(["git", *args], capture_output=True, timeout=300, cwd=cwd)
    return r.returncode == 0


def noisy(path: str) -> bool:
    return path in NOISE or path.startswith(NOISE_PREFIX)


def parse_date(text: str) -> dt.datetime | None:
    """A `committerdate:iso-strict` value, or None."""
    text = text.strip()
    if text.endswith("Z"):  # git may write UTC as Z; Python 3.10 does not read it
        text = text[:-1] + "+00:00"
    try:
        return dt.datetime.fromisoformat(text)
    except ValueError:
        return None


def gh_pulls(cwd: str | None = None) -> dict[str, dict]:
    """Pull requests by head branch, empty when gh is missing or unauthorised."""
    if not shutil.which("gh"):
        return {}
    try:
        r = subprocess.run(
            ["gh", "pr", "list", "--state", "open", "--limit", "100",
             "--json", "number,headRefName,mergeable,isDraft,title"],
            capture_output=True, timeout=60, cwd=cwd)
    except (OSError, subprocess.TimeoutExpired):
        return {}
    if r.returncode != 0:
        return {}
    try:
        return {p["headRefName"]: p for p in json.loads(r.stdout.decode("utf-8"))}
    except (json.JSONDecodeError, KeyError, TypeError):
        return {}


def fetch(cwd: str | None = None) -> None:
    """Fetch every branch of origin. A failure is reported, not fatal."""
    if not git_ok("fetch", "--prune", "--quiet", "origin", REFSPEC, cwd=cwd):
        print("Note: git fetch failed; the report uses the refs already here.",
              file=sys.stderr)


def deepen(cwd: str | None = None) -> bool:
    """Try to make merge bases reachable in a shallow clone.

    First a bounded `--deepen`, then `--unshallow`. Returns True when either
    worked. Only called when a branch was skipped for a missing merge base.
    """
    if git("rev-parse", "--is-shallow-repository", cwd=cwd) != "true":
        return False
    if git_ok("fetch", "--quiet", f"--deepen={DEEPEN}", "origin", REFSPEC, cwd=cwd):
        return True
    if git_ok("fetch", "--quiet", "--unshallow", "origin", REFSPEC, cwd=cwd):
        return True
    print("Note: could not deepen the shallow clone (no network or not "
          "allowed).", file=sys.stderr)
    return False


def collect(max_age_days: int = 0, pulls: dict | None = None,
            cwd: str | None = None) -> tuple[list[dict], list[str]]:
    """(open branches, skipped branch names) against MAIN."""
    raw = git("for-each-ref",
              "--format=%(refname:short)%09%(committerdate:iso-strict)",
              "refs/remotes/origin", cwd=cwd)
    now = dt.datetime.now(dt.timezone.utc)
    pulls = pulls or {}
    branches, skipped = [], []
    for line in raw.splitlines():
        if "\t" not in line:
            continue
        ref, when = line.split("\t", 1)
        if ref in (MAIN, "origin", "origin/HEAD") or ref.endswith("/HEAD"):
            continue
        # Merged branches are not pending work, only clutter.
        if git_ok("merge-base", "--is-ancestor", ref, MAIN, cwd=cwd):
            continue
        base = git("merge-base", ref, MAIN, cwd=cwd)
        if not base:
            # No common ancestor in reach: usually a shallow clone. Never
            # drop this silently, or the report reads "all clear".
            skipped.append(ref.removeprefix("origin/"))
            continue
        files = [f for f in git("diff", "--name-only", f"{base}..{ref}",
                                cwd=cwd).splitlines() if f]
        ahead = git("rev-list", "--count", f"{base}..{ref}", cwd=cwd)
        last = parse_date(when)
        age = (now - last.astimezone(dt.timezone.utc)).days if last else -1
        if max_age_days and age < max_age_days:
            continue
        short = ref.removeprefix("origin/")
        branches.append({
            "ref": ref, "short": short, "age": age,
            "ahead": int(ahead or 0), "files": files, "pr": pulls.get(short),
        })
    return branches, skipped


def report(branches: list[dict], skipped: list[str], show_paths: bool) -> None:
    if skipped:
        print(f"WARNING: {len(skipped)} branch(es) skipped, no common ancestor "
              f"with {MAIN} in this clone:")
        for name in sorted(skipped):
            print(f"  {name}")
        print("This is usually a shallow clone. Deepen it and run again:\n"
              f"  git fetch --deepen={DEEPEN} origin '{REFSPEC}'\n"
              "  (or: git fetch --unshallow origin, or run with --fetch)\n")

    if not branches:
        if skipped:
            print("No other open branches found, but the skipped ones above "
                  "were not checked.")
        else:
            print("No open branches. main has everything.")
        return

    branches.sort(key=lambda b: -b["age"])

    # Which file is touched by more than one branch? That is the collision that
    # produces duplicate work, and it is the reason this script exists.
    owners: dict[str, list[str]] = collections.defaultdict(list)
    for b in branches:
        for f in b["files"]:
            if not noisy(f):
                owners[f].append(b["short"])
    collisions = {f: bs for f, bs in owners.items() if len(bs) > 1}

    print(f"{len(branches)} open branch(es) against {MAIN}:\n")
    for b in branches:
        pr = b["pr"]
        tag = f"PR #{pr['number']}" if pr else "no PR"
        if pr and pr.get("isDraft"):
            tag += ", draft"
        if pr and pr.get("mergeable") == "CONFLICTING":
            tag += ", CONFLICT"
        agetxt = f"{b['age']} days old" if b["age"] >= 0 else "age unknown"
        print(f"  {b['short']}")
        print(f"      {agetxt}, {b['ahead']} commit(s), {len(b['files'])} file(s), {tag}")
        if pr:
            print(f"      {pr['title']}")
        if show_paths:
            for f in b["files"]:
                print(f"        {f}")
        print()

    if collisions:
        print(f"WARNING: {len(collisions)} file(s) are on more than one branch.")
        print("This is where duplicate work happens. Read the other branch before writing.\n")
        for f, bs in sorted(collisions.items()):
            print(f"  {f}")
            for name in bs:
                print(f"      {name}")
        print()
    else:
        print("No file is on two branches at once.\n")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--fetch", action="store_true",
                    help="fetch every branch of origin first (and deepen a "
                         "shallow clone if a branch needs it)")
    ap.add_argument("--paths", action="store_true", help="list every changed file")
    ap.add_argument("--strict", action="store_true",
                    help="exit 1 when branches are open or had to be skipped")
    ap.add_argument("--max-age-days", type=int, default=0,
                    help="only branches whose last commit is at least this old")
    ap.add_argument("--no-gh", action="store_true",
                    help="do not ask the GitHub CLI for pull requests")
    args = ap.parse_args(argv)

    if args.fetch:
        fetch()

    if not git("rev-parse", "--verify", "--quiet", MAIN):
        print(f"{MAIN} not found. No remote, or never fetched.", file=sys.stderr)
        return 1 if args.strict else 0

    pulls = {} if args.no_gh else gh_pulls()
    branches, skipped = collect(args.max_age_days, pulls)
    if skipped and args.fetch and deepen():
        branches, skipped = collect(args.max_age_days, pulls)

    report(branches, skipped, args.paths)
    if args.strict and (branches or skipped):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""What lies on branches that `main` does not have yet.

A session that only reads the working tree cannot see work that is finished
but unmerged, and the repository's own rules push work into that blind spot:
a task ends with a pull request, branches are pushed early and often, and
nothing merges them again. Without this check, two sessions move the same
capture to two different places, or build against a decision that sits
unmerged on another branch.

So: run this **before** triage, before creating a canonical file, and before
building a mechanism. It answers one question. *Has somebody already done
this, on a branch I am not standing on?*

Deliberately branch-based, not pull-request-based. Branches need no token and
no network service, they work in every checkout including scheduled cloud
runs, and a branch may carry work without any pull request at all. When `gh`
happens to be available and authenticated, the pull-request number and its
mergeability are added on top; without it the report is complete, just less
convenient.

Exit code is 0 unless --strict is given: this is a briefing, not a gate.

  python3 00-system/scripts/branch_overview.py
  python3 00-system/scripts/branch_overview.py --fetch      # git fetch first
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


def git(*args: str, ok_fail: bool = False) -> str:
    r = subprocess.run(["git", *args], capture_output=True, timeout=120)
    if r.returncode != 0 and not ok_fail:
        return ""
    return r.stdout.decode("utf-8", "replace").strip()


def noisy(path: str) -> bool:
    return path in NOISE or path.startswith(NOISE_PREFIX)


def gh_pulls() -> dict[str, dict]:
    """Pull requests by head branch, empty when gh is missing or unauthorised."""
    if not shutil.which("gh"):
        return {}
    r = subprocess.run(
        ["gh", "pr", "list", "--state", "open", "--limit", "100",
         "--json", "number,headRefName,mergeable,isDraft,title"],
        capture_output=True, timeout=60)
    if r.returncode != 0:
        return {}
    try:
        return {p["headRefName"]: p for p in json.loads(r.stdout.decode("utf-8"))}
    except (json.JSONDecodeError, KeyError, TypeError):
        return {}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fetch", action="store_true", help="git fetch --prune first")
    ap.add_argument("--paths", action="store_true", help="list every changed file")
    ap.add_argument("--strict", action="store_true", help="exit 1 when branches are open")
    ap.add_argument("--max-age-days", type=int, default=0,
                    help="only branches whose last commit is at least this old")
    args = ap.parse_args()

    if args.fetch:
        subprocess.run(["git", "fetch", "--prune", "--quiet"], timeout=300)

    if not git("rev-parse", "--verify", "--quiet", MAIN):
        print(f"{MAIN} not found. No remote, or never fetched.", file=sys.stderr)
        return 0

    raw = git("for-each-ref", "--format=%(refname:short)%09%(committerdate:iso8601)",
              "refs/remotes/origin")
    today = dt.datetime.now(dt.timezone.utc)
    pulls = gh_pulls()

    branches = []
    for line in raw.splitlines():
        if "\t" not in line:
            continue
        ref, when = line.split("\t", 1)
        if ref in (MAIN, "origin/HEAD") or ref.endswith("/HEAD"):
            continue
        # Merged branches are not pending work, only clutter.
        if subprocess.run(["git", "merge-base", "--is-ancestor", ref, MAIN],
                          capture_output=True).returncode == 0:
            continue

        base = git("merge-base", ref, MAIN)
        if not base:
            continue
        files = [f for f in git("diff", "--name-only", f"{base}..{ref}").splitlines() if f]
        ahead = git("rev-list", "--count", f"{base}..{ref}")
        try:
            last = dt.datetime.fromisoformat(when.replace(" ", "T", 1).replace(" ", ""))
            age = (today - last.astimezone(dt.timezone.utc)).days
        except ValueError:
            age = -1
        if args.max_age_days and age < args.max_age_days:
            continue
        branches.append({
            "ref": ref, "short": ref.removeprefix("origin/"), "age": age,
            "ahead": int(ahead or 0), "files": files,
            "pr": pulls.get(ref.removeprefix("origin/")),
        })

    if not branches:
        print("No open branches. main has everything.")
        return 0

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
        if args.paths:
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

    return 1 if args.strict else 0


if __name__ == "__main__":
    raise SystemExit(main())

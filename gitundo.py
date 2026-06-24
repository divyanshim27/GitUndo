#!/usr/bin/env python3
"""
git-undo: an interactive safety net for the git mistakes everyone makes.

No new mental model to learn — just a menu of plain-English undo actions,
each one printed before it runs, with a hard confirmation on anything
destructive.

Usage:
    python git_undo.py            # interactive menu
    python git_undo.py --list     # print available actions, run nothing
"""
from __future__ import annotations

import argparse
import subprocess

DESTRUCTIVE = {"hard-reset-commit", "discard-changes", "reset-to-orig-head"}

ACTIONS = [
    ("undo-commit-keep-changes", "Undo last commit, keep changes staged",
     ["git", "reset", "--soft", "HEAD~1"]),
    ("hard-reset-commit", "Undo last commit, DISCARD changes",
     ["git", "reset", "--hard", "HEAD~1"]),
    ("unstage-all", "Unstage all staged files (keep changes in working dir)",
     ["git", "reset"]),
    ("discard-changes", "DISCARD all uncommitted changes in working dir",
     ["git", "checkout", "--", "."]),
    ("pop-stash", "Apply and remove the most recent stash",
     ["git", "stash", "pop"]),
    ("reset-to-orig-head", "Undo last pull/merge (reset to ORIG_HEAD), DISCARDING changes",
     ["git", "reset", "--hard", "ORIG_HEAD"]),
    ("amend-message", "Amend the last commit message",
     ["git", "commit", "--amend"]),
    ("show-reflog", "Show reflog so you can manually find a commit to recover",
     ["git", "reflog", "-20"]),
]


def run(cmd: list[str]) -> None:
    print(f"\n$ {' '.join(cmd)}\n")
    subprocess.run(cmd)


def main():
    parser = argparse.ArgumentParser(description="Interactive undo menu for common git mistakes.")
    parser.add_argument("--list", action="store_true", help="List actions and exit, run nothing")
    args = parser.parse_args()

    if args.list:
        for key, desc, _cmd in ACTIONS:
            print(f"{key:<22} {desc}")
        return

    print("git-undo — what do you want to undo?\n")
    for i, (key, desc, _cmd) in enumerate(ACTIONS, 1):
        flag = " ⚠ destructive" if key in DESTRUCTIVE else ""
        print(f"  {i}. {desc}{flag}")
    print("  0. Cancel")

    choice = input("\n> ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(ACTIONS)):
        print("Cancelled.")
        return

    key, desc, cmd = ACTIONS[int(choice) - 1]

    if key in DESTRUCTIVE:
        confirm = input(
            f"This will run: {' '.join(cmd)}\nThis cannot be undone. Type 'yes' to continue: "
        )
        if confirm.strip().lower() != "yes":
            print("Cancelled.")
            return

    run(cmd)


if __name__ == "__main__":
    main()
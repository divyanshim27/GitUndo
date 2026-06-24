# git-undo

An interactive menu for the git mistakes everyone makes — instead of
googling "how to undo git commit" at midnight.

No new mental model to learn. Pick a number, see the exact `git` command
before it runs, confirm anything destructive.

## Usage

```bash
python git_undo.py            # interactive menu
python git_undo.py --list     # see all actions, run nothing
```

## What it covers

```
1. Undo last commit, keep changes staged
2. Undo last commit, DISCARD changes              ⚠ destructive
3. Unstage all staged files (keep changes in working dir)
4. DISCARD all uncommitted changes in working dir  ⚠ destructive
5. Apply and remove the most recent stash
6. Undo last pull/merge (reset to ORIG_HEAD)       ⚠ destructive
7. Amend the last commit message
8. Show reflog so you can manually find a commit to recover
```

Every "destructive" action requires typing `yes` to confirm before it runs.

## License

MIT
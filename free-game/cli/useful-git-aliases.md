# Useful Git Aliases

Time-saving Git aliases to add to your `~/.gitconfig`.

## Setup

Add these to your `~/.gitconfig` file under the `[alias]` section:

```ini
[alias]
    # Status shortcuts
    st = status
    s = status -sb

    # Commit shortcuts
    c = commit
    cm = commit -m
    ca = commit --amend
    can = commit --amend --no-edit

    # Branch operations
    br = branch
    co = checkout
    cob = checkout -b
    sw = switch
    swc = switch -c

    # Log viewing
    lg = log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit
    last = log -1 HEAD
    ll = log --oneline -10

    # Diff shortcuts
    d = diff
    dc = diff --cached
    ds = diff --stat

    # Stash operations
    stash-all = stash save --include-untracked

    # Undo operations
    undo = reset --soft HEAD~1
    unstage = reset HEAD --

    # Remote operations
    pushf = push --force-with-lease
    syncfork = !git fetch upstream && git merge upstream/main

    # Cleanup
    cleanup = !git branch --merged | grep -v '\\*\\|main\\|master\\|develop' | xargs -n 1 git branch -d
    prune-local = !git fetch -p && git branch -vv | awk '/: gone]/{print $1}' | xargs git branch -D

    # Useful info
    aliases = config --get-regexp alias
    contributors = shortlog --summary --numbered
    today = log --since='midnight' --author='$(git config user.email)' --oneline
```

## Most Useful Aliases

### Quick Status
```bash
git s
# Shows: ## main...origin/main [ahead 1]
#        M  file.txt
#        ?? new-file.txt
```

### Pretty Log
```bash
git lg
# Shows: * a1b2c3d - (HEAD -> main) Added feature (2 hours ago) <Your Name>
```

### Safe Force Push
```bash
git pushf
# Safer than --force, won't overwrite others' work
```

### Cleanup Merged Branches
```bash
git cleanup
# Deletes all local branches that have been merged
```

### Quick Amend
```bash
git can
# Amend last commit without editing message
```

## Custom Functions

Add more complex operations to your `.gitconfig`:

```ini
[alias]
    # Find commits by message
    find = "!f() { git log --all --oneline --grep=\"$1\"; }; f"

    # Show contributors and their commits
    who = "!f() { git log --author=\"$1\" --oneline; }; f"

    # Interactive rebase with N commits
    rb = "!f() { git rebase -i HEAD~$1; }; f"

    # Create branch from issue number
    issue = "!f() { git checkout -b issue-$1; }; f"
```

Usage:
```bash
git find "bug fix"
git who "Alice"
git rb 3  # Interactive rebase last 3 commits
git issue 123  # Creates branch 'issue-123'
```

# 🚀 Day 70: Git, GitHub, and Version Control

## 🧽 Overview

A concise guide to using Git and GitHub for version control, collaboration, and repository management.

---

## 🪰 Topics Covered

- Common Git commands
- Creating and connecting to remote repositories
- Using `.gitignore` effectively
- Branching and merging strategies
- Cloning vs forking
- Understanding pull and push requests

---

## 🛠️ Git Commands

```bash
git status               # Show current changes and branch info
git init                 # Initialize a Git repository
git add .                # Stage all changes
git commit -m "message"  # Commit changes with a message
git push                 # Push to the default remote
git push origin main -u  # Push to remote and set upstream
git rm --cached -r .     # Unstage files (undo `git add`)
git log                  # Show commit history
clear                    # Clear terminal screen
```

> To exit `git log`, press `q`.

---

## 🌐 Creating a Remote Repository

```bash
git remote add <name> <url>         # Connect local repo to GitHub
git push -u <remote-name> <branch>  # Push initial commit and set upstream
```

---

## 📄 Creating Files and .gitignore

```bash
touch <filename>         # Create a new file
touch .gitignore         # Create a .gitignore file
code .gitignore          # Open .gitignore in VSCode (optional)
```

### Example `.gitignore`:

```
# Node modules
node_modules/

# Logs
*.log

# OS-generated files
.DS_Store
Thumbs.db

# Environment files
.env
```

---

## 🌿 Branching and Merging

### Create a Branch

```bash
git branch <branch-name>  # Create a new branch
git branch                # List all branches (current is highlighted)
```

### Switch to a Branch

```bash
git checkout <branch-name>  # Switch to the desired branch
```

### Merge a Branch

```bash
git checkout main           # Switch to main branch
git merge <branch-name>     # Merge changes from other branch into main
```

> If VIM opens, type `:q!` to exit the message editor.

---

## 🔁 Cloning vs Forking

### Git Clone

- Duplicates the entire repository locally.
- Ideal for internal collaboration with team members who have push access.

```bash
git clone <url>
```

### Git Fork

- Makes a personal copy of a remote repository on GitHub.
- Useful for open source or contributing without write access.
- You can make changes independently and submit them via a Pull Request.

---

## 🔄 Pull vs Push Requests

### Pull Request (PR)

- A GitHub feature for proposing changes from one repo/branch to another.
- Used to suggest improvements, bug fixes, or features.
- Reviewed and merged by the repository owner.

### Push "Request"

> ⚠️ Not an official Git/GitHub term.

- Refers informally to pushing changes to your own or shared remote.
- No approval is needed if you have write access.

---

## ✅ Quick Reference Checklist

- ***

## 📚 Further Reading

- [Git Documentation](https://git-scm.com/doc)
- [GitHub Docs](https://docs.github.com/en)
- Markdown Cheatsheet

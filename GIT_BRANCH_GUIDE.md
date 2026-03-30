# Git Branch Guide

A quick reference for creating, naming, and pushing branches to GitHub.

---

## 1. Make Sure You're Up to Date

Before creating a new branch, always pull the latest changes from main:

```bash
git checkout main
git pull origin main
```

---

## 2. Create a New Branch

```bash
git checkout -b <branch-name>
```

**Example:**
```bash
git checkout -b update/gmail-smtp-password-reset-dbfill-update
```

This creates the branch AND switches to it in one command.

---

## 3. Branch Naming Convention

Use this format: `<type>/<short-description>`

| Type | When to Use |
|------|-------------|
| `update/` | Adding or improving existing features |
| `feature/` | Brand new feature |
| `fix/` | Bug fix |
| `hotfix/` | Urgent production fix |
| `refactor/` | Code cleanup, no new features |

**Examples:**
```
update/sidebar-navigation-button-update
feature/email-notifications
fix/login-401-error
hotfix/payment-crash
refactor/cleanup-api-routes
```

Rules:
- All **lowercase**
- Use **hyphens** instead of spaces
- Keep it **short but descriptive**

---

## 4. Make Your Changes

Edit your files, then stage and commit:

```bash
# Stage all changes
git add .

# Or stage a specific file
git add frontend/js/menu.js

# Commit with a descriptive message
git commit -m "Short description of what was changed"
```

**Good commit message examples:**
```
git commit -m "Add Gmail SMTP for password reset emails"
git commit -m "Fix: sidebar close button overlapping title on desktop"
git commit -m "Feature: fill database with seed data on startup"
```

---

## 5. Push the Branch to GitHub

```bash
git push -u origin <branch-name>
```

**Example:**
```bash
git push -u origin update/gmail-smtp-password-reset-dbfill-update
```

The `-u` flag sets the upstream so next time you can just run `git push`.

---

## 6. Create a Pull Request (PR)

After pushing, GitHub will print a link in the terminal:

```
remote: Create a pull request by visiting:
remote:   https://github.com/your-repo/pull/new/your-branch-name
```

Open that link in your browser to create a PR and merge into main.

---

## Quick Reference Cheatsheet

```bash
# 1. Start from main
git checkout main
git pull origin main

# 2. Create and switch to new branch
git checkout -b update/your-branch-name

# 3. Make changes, then stage and commit
git add .
git commit -m "Your commit message"

# 4. Push to GitHub
git push -u origin update/your-branch-name
```

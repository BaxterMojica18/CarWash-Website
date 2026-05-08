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
git checkout -b feature/websocket-queue-05-08-2026
```

This creates the branch AND switches to it in one command.

---

## 3. Branch Naming Convention

Use this format: `<type>/<short-description>-<MM-DD-YYYY>`

The date suffix is **today's date** in MM-DD-YYYY format.

| Type | When to Use | Example |
|------|-------------|---------|
| `feature/` | Brand new feature | `feature/email-notifications-05-08-2026` |
| `bugfix/` | Bug fix | `bugfix/login-401-error-05-08-2026` |
| `hotfix/` | Urgent production fix | `hotfix/payment-crash-05-08-2026` |

Rules:
- All **lowercase**
- Use **hyphens** instead of spaces
- Keep it **short but descriptive**
- Always append **today's date** as `-MM-DD-YYYY`

---

## 4. Make Your Changes

Edit your files, then stage and commit:

```bash
# Stage specific files (NEVER use git add .)
git add app/routers/orders.py app/schemas.py frontend/orders.html

# Commit with the *CODE UPDATE* format
git commit -m "*CODE UPDATE*
- Added order status endpoint for real-time tracking.
- Updated order schema with delivery_date field.
- Created orders page with status timeline UI."
```

### Commit Message Format

```
*CODE UPDATE*
- Change description ending with a period.
- Another change description ending with a period.
```

**Rules:**
- First line is always `*CODE UPDATE*`
- Each change starts with `- ` on a new line
- Each change is exactly **one sentence ending with a period**
- List ALL changes from the session
- Be descriptive — explain what was done, not just which file

---

## 5. Push the Branch to GitHub

```bash
git push -u origin feature/<branch-name>-<MM-DD-YYYY>
```

**Example:**
```bash
git push -u origin feature/websocket-queue-05-08-2026
```

The `-u` flag sets the upstream so next time you can just run `git push`.

---

## 6. Merge to Main and Push

After pushing your branch, merge it to main:

```bash
git checkout main
git merge feature/<branch-name>-<MM-DD-YYYY>
git push origin main
```

**NEVER push directly to main without creating a branch first.**

---

## Full Push Workflow (Strict Sequence)

```bash
# 1. Start from main
git checkout main
git pull origin main

# 2. Create and switch to new branch (with today's date)
git checkout -b feature/your-feature-name-05-08-2026

# 3. Make changes, then stage SPECIFIC files (never git add .)
git add app/routers/feature.py app/schemas.py frontend/feature.html frontend/js/feature.js

# 4. Commit with *CODE UPDATE* format
git commit -m "*CODE UPDATE*
- Added feature endpoint with proper auth guards.
- Created Pydantic schemas for request/response validation.
- Built feature page with sidebar integration.
- Added client-side API calls using api.js module."

# 5. Push branch to GitHub
git push -u origin feature/your-feature-name-05-08-2026

# 6. Merge to main and push
git checkout main
git merge feature/your-feature-name-05-08-2026
git push origin main
```

---

## Important Rules

- **Never force push** — if push is rejected, run `git pull --no-rebase` first
- **Never push directly to main** — always create a branch first
- **Never use `git add .`** — stage specific files to avoid committing unrelated changes
- **Always use `-u` flag** on first push of a new branch
- **Always include date suffix** on branch names for traceability

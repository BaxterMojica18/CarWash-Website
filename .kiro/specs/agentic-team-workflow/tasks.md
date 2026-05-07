# Implementation Plan: Agentic Team Workflow

## Overview

This plan implements the Micro-SaaS Agentic Team workflow system through Kiro configuration files. The implementation creates a Master Orchestrator steering file, 5 automation hooks, 4 role playbooks, and updates the existing GIT_BRANCH_GUIDE.md to reflect the new git conventions. Each task creates specific files with defined content — no application code is involved.

## Tasks

- [ ] 1. Create the Orchestrator Steering File
  - [ ] 1.1 Create `.kiro/steering/orchestrator.md` with frontmatter `inclusion: auto`
    - Include Session Protocol section: rules for reading `PROJECT_ROADMAP.md`, `SYSTEM_UPDATES_DATA_HISTORY_LOGS.md`, and `GIT_BRANCH_GUIDE.md` at session start
    - Include session summary format (current version, last session date, next roadmap item)
    - Include Execution Loop section defining phases: Context Load → Ideation → Delegation → Development → Testing → Documentation
    - Include Delegation Protocol section with Delegation_Payload format (target agent, task, scope, acceptance criteria, dependencies)
    - Include Role Dispatch Rules section mapping task types to role playbooks
    - Include Git Workflow section with branch naming (`feature/<name>-<MM-DD-YYYY>`, `bugfix/<name>-<MM-DD-YYYY>`), commit message format (`*CODE UPDATE*` header, `- ` prefixed changes), and push workflow (branch → stage → commit → push → merge to main → push main)
    - Include Error Handling section with recovery procedures and escalation rules (3 retries then escalate to user)
    - Include reference to existing `.agents/workflows/instructions.md` as foundation
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 6.1, 6.2, 6.3, 6.4, 6.5, 7.4, 7.5, 8.1, 8.2, 8.3, 8.4, 8.5, 8.6, 9.1, 9.2, 9.3, 9.4, 9.5, 10.1, 10.5_

- [ ] 2. Create Hook Configuration Files
  - [ ] 2.1 Create `.kiro/hooks/session-context-load.json`
    - Event: `promptSubmit`, Action: `askAgent`
    - Output prompt instructs reading PROJECT_ROADMAP.md, SYSTEM_UPDATES_DATA_HISTORY_LOGS.md, GIT_BRANCH_GUIDE.md
    - Instructs producing a 2-line session summary with current version and next planned item
    - _Requirements: 1.1, 1.2, 1.3, 1.5_

  - [ ] 2.2 Create `.kiro/hooks/doc-update-reminder.json`
    - Event: `agentStop`, Action: `askAgent`
    - Output prompt instructs verifying SYSTEM_UPDATES_DATA_HISTORY_LOGS.md has new session entry
    - Instructs verifying PROJECT_ROADMAP.md has completed items marked with [x]
    - Instructs verifying version numbers are updated if features were completed
    - _Requirements: 7.1, 7.2, 7.3_

  - [ ] 2.3 Create `.kiro/hooks/git-safety-check.json`
    - Event: `preToolUse`, Action: `askAgent`, Tool Types: `shell`
    - Output prompt enforces branch naming: `feature/<name>-MM-DD-YYYY` for features, `bugfix/<name>-MM-DD-YYYY` for bug fixes
    - Enforces never pushing directly to main — always branch first, then merge
    - Enforces commit message format: `*CODE UPDATE*` header with `- ` prefixed changes ending in periods
    - Enforces `-u` flag for first push and staging specific files (not `git add .`)
    - _Requirements: 8.1, 8.2, 8.4, 8.5, 8.6_

  - [ ] 2.4 Create `.kiro/hooks/post-task-qa.json`
    - Event: `postTaskExecution`, Action: `askAgent`
    - Output prompt triggers QA validation: identify changes, run relevant tests, verify multi-tenant isolation, check for regressions
    - _Requirements: 5.1, 5.2, 5.3, 5.6_

  - [ ] 2.5 Create `.kiro/hooks/backend-file-watch.json`
    - Event: `fileEdited`, Action: `askAgent`, File Patterns: `app/**/*.py`
    - Output prompt validates: business_number scoping, Pydantic schemas usage, router patterns, env var documentation
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_

- [ ] 3. Checkpoint - Verify hook and steering file configuration
  - Ensure all JSON hook files are valid JSON with required fields (name, description, eventType, hookAction, outputPrompt)
  - Ensure steering file has correct YAML frontmatter with `inclusion: auto`
  - Ask the user if questions arise.

- [ ] 4. Create Role Playbook Files
  - [ ] 4.1 Create `.agents/workflows/roles/cto-agent.md`
    - Define Role Identity: architecture review, implementation planning, task decomposition
    - Define Constraints: must validate against existing tech stack (Python FastAPI, PostgreSQL, vanilla HTML/CSS/JS, JWT + Firebase Auth, Stripe, Resend API)
    - Define Input Format: receives ideation task from Orchestrator with roadmap item reference
    - Define Output Format: implementation plan with affected files, database changes, and decomposed tasks for Backend/Frontend agents
    - Define conflict detection and alternative proposal rules
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_

  - [ ] 4.2 Create `.agents/workflows/roles/backend-agent.md`
    - Define Role Identity: Python/FastAPI development, database migrations, API endpoints
    - Define Constraints: follow existing patterns in `app/`, create migrations in `commands/database/`, use Pydantic schemas, scope by business_number
    - Define Input Format: Delegation_Payload with files to modify, acceptance criteria
    - Define Output Format: list of created/modified files, status report to Orchestrator
    - Define rules for env var documentation and `.env.example` updates
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6_

  - [ ] 4.3 Create `.agents/workflows/roles/frontend-agent.md`
    - Define Role Identity: vanilla HTML/CSS/JS development, UI patterns, responsiveness
    - Define Constraints: use `frontend/js/api.js` for API calls, integrate `frontend/js/menu.js` sidebar, include standard page elements (sidebar, profile dropdown, no-cache headers)
    - Define Input Format: Delegation_Payload with files to modify, acceptance criteria
    - Define Output Format: list of created/modified files, status report to Orchestrator
    - Define mobile-first responsive rules (edge-tap sidebar, bottom navigation)
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6_

  - [ ] 4.4 Create `.agents/workflows/roles/qa-agent.md`
    - Define Role Identity: pytest testing, validation, deployment gatekeeping
    - Define Constraints: write pytest test cases, validate status codes, verify multi-tenant isolation, run full test suite from `commands/testing/`
    - Define Input Format: QA task from Orchestrator with list of changes to validate
    - Define Output Format: pass/fail status with failure details and recommended fixes
    - Define escalation rules (report failures to Orchestrator, approve on all-pass)
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6_

- [ ] 5. Update GIT_BRANCH_GUIDE.md with New Conventions
  - [ ] 5.1 Update `GIT_BRANCH_GUIDE.md` to reflect the new git conventions
    - Update branch naming to use date suffix format: `feature/<feature-name>-<MM-DD-YYYY>`, `bugfix/<bugfix-name>-<MM-DD-YYYY>`
    - Add the `*CODE UPDATE*` commit message format with `- ` prefixed changes ending in periods
    - Update the push workflow to include the full sequence: create branch → stage files → commit → push branch → merge to main → push main
    - Keep existing content that doesn't conflict (pull latest, -u flag, lowercase/hyphens rules)
    - Remove or update examples that conflict with new conventions
    - _Requirements: 7.4, 7.5, 8.1, 8.2, 8.4, 8.5, 8.6_

- [ ] 6. Update .gitignore to Exclude Reference and Test Files from Deployment
  - [ ] 6.1 Add workflow/reference markdown files to `.gitignore`
    - Add `.kiro/` directory (specs, steering, hooks — dev tooling only)
    - Add `.agents/` directory (workflow instructions, role playbooks)
    - Add `PROJECT_ROADMAP.md` (internal roadmap tracking)
    - Add `SYSTEM_UPDATES_DATA_HISTORY_LOGS.md` (internal session history)
    - Add `GIT_BRANCH_GUIDE.md` (internal git reference)
    - Add `sidebar_visibility_refactor_summary.md` (internal refactor notes)
  - [ ] 6.2 Add pytest/test files to `.gitignore`
    - Add `commands/testing/` directory
    - Add `.pytest_cache/`
    - Add `conftest.py`
    - Add `pytest.ini`
    - Verify existing `test_*.py` pattern is already present (it is)
  - [ ] 6.3 Update `.dockerignore` to match the same exclusions
    - Ensure Docker builds don't include reference markdown files or test scripts
    - _Requirements: Design — Deployment Exclusion section_

- [ ] 7. Final Checkpoint - Validate complete configuration
  - Verify all files exist at their expected paths
  - Verify hook JSON files reference valid Kiro event types (`promptSubmit`, `agentStop`, `preToolUse`, `postTaskExecution`, `fileEdited`)
  - Verify role playbooks are referenced correctly from the Orchestrator steering file
  - Verify GIT_BRANCH_GUIDE.md reflects the new conventions consistently with the hooks and steering file
  - Verify `.gitignore` excludes all reference markdown and pytest files
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- No property-based tests are included — this feature consists entirely of configuration files (JSON, Markdown) with no algorithmic logic to test
- The existing `.agents/workflows/instructions.md` remains unchanged and is referenced by the Orchestrator as a foundation
- All hook JSON files must have valid structure with required fields: `name`, `description`, `eventType`, `hookAction`, `outputPrompt`
- The steering file frontmatter (`inclusion: auto`) is critical — without it, the Orchestrator won't auto-load
- Each task references specific requirement acceptance criteria for traceability
- All reference/workflow markdown files and pytest files are excluded from deployment via `.gitignore` and `.dockerignore` — they exist locally only for the agentic workflow

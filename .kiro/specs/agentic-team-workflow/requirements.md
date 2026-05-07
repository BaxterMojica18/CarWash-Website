# Requirements Document

## Introduction

This feature formalizes a structured development workflow for the Car Wash Management System using specialized AI agent roles (a "Micro-SaaS Agentic Team"). This is a development process automation that structures how Kiro operates on this project — not a user-facing code feature. The workflow defines a Master Orchestrator (CEO/DevOps Agent) that coordinates specialized sub-agents (CTO, Backend Developer, Frontend Developer, QA Tester) through a repeatable execution loop, ensuring every development session consults existing documentation, follows git conventions, and updates project history.

## Glossary

- **Orchestrator**: The primary coordinating agent (CEO/DevOps role) that manages session state, delegates tasks, and handles deployment routines
- **CTO_Agent**: The specialized agent responsible for system architecture decisions, ideation, and roadmap management
- **Backend_Agent**: The specialized agent responsible for Python/FastAPI core logic, database migrations, and API development
- **Frontend_Agent**: The specialized agent responsible for UI/UX implementation, client-side logic, and SEO (currently vanilla HTML/CSS/JS, future Next.js)
- **QA_Agent**: The specialized agent responsible for automated testing, code validation, and deployment gatekeeping using pytest
- **Session**: A single development interaction from context loading through task completion to documentation update
- **Context_Files**: The set of reference documents consulted every session: `PROJECT_ROADMAP.md`, `GIT_BRANCH_GUIDE.md`, `SYSTEM_UPDATES_DATA_HISTORY_LOGS.md`
- **Execution_Loop**: The repeatable sequence of steps (Context Load → Ideation → Delegation → Development → Testing → Documentation) that governs each session
- **Delegation_Payload**: The structured task description passed from the Orchestrator to a specialized agent, including scope, files to modify, and acceptance criteria

## Requirements

### Requirement 1: Session Context Initialization

**User Story:** As a developer, I want the Orchestrator to automatically load project context at the start of every session, so that all development decisions are informed by the current state of the system.

#### Acceptance Criteria

1. WHEN a new session begins, THE Orchestrator SHALL read `PROJECT_ROADMAP.md` to determine the current version and next planned features
2. WHEN a new session begins, THE Orchestrator SHALL read `SYSTEM_UPDATES_DATA_HISTORY_LOGS.md` to understand the latest changes and active version number
3. WHEN a new session begins, THE Orchestrator SHALL read `GIT_BRANCH_GUIDE.md` to confirm branch naming conventions before any git operations
4. IF any Context_File is missing or unreadable, THEN THE Orchestrator SHALL report the missing file and halt further operations until the issue is resolved
5. WHEN context loading completes, THE Orchestrator SHALL produce a brief session summary stating the current version, last session date, and the next roadmap item

### Requirement 2: CTO Agent — Architecture and Ideation

**User Story:** As a developer, I want a CTO Agent that reviews the roadmap and proposes implementation plans, so that development follows a coherent architectural direction.

#### Acceptance Criteria

1. WHEN the Orchestrator delegates an ideation task, THE CTO_Agent SHALL review the next uncompleted item in `PROJECT_ROADMAP.md`
2. WHEN reviewing a roadmap item, THE CTO_Agent SHALL produce an implementation plan that identifies affected backend files, frontend files, and database changes
3. THE CTO_Agent SHALL validate that proposed changes are compatible with the existing tech stack (Python FastAPI, PostgreSQL, vanilla HTML/CSS/JS, JWT + Firebase Auth, Stripe, Resend API)
4. IF a proposed feature conflicts with existing architecture, THEN THE CTO_Agent SHALL flag the conflict and propose an alternative approach
5. WHEN the implementation plan is approved, THE CTO_Agent SHALL decompose the work into discrete tasks suitable for delegation to Backend_Agent and Frontend_Agent

### Requirement 3: Backend Agent — API and Database Development

**User Story:** As a developer, I want a Backend Agent that handles all server-side implementation, so that API endpoints, database migrations, and business logic are developed consistently.

#### Acceptance Criteria

1. WHEN the Orchestrator delegates a backend task, THE Backend_Agent SHALL implement changes using Python FastAPI conventions matching the existing codebase patterns in `app/`
2. THE Backend_Agent SHALL create database migration scripts in `commands/database/` for any schema changes rather than modifying tables directly
3. WHEN creating new API endpoints, THE Backend_Agent SHALL follow the existing router pattern in `app/routers/` with proper Pydantic schemas in `app/schemas.py`
4. THE Backend_Agent SHALL scope all data queries by `business_number` to maintain multi-tenant isolation
5. IF a backend task requires new environment variables, THEN THE Backend_Agent SHALL document them in the task output and update `.env.example`
6. WHEN implementation is complete, THE Backend_Agent SHALL provide a list of all created and modified files to the Orchestrator

### Requirement 4: Frontend Agent — UI and Client-Side Development

**User Story:** As a developer, I want a Frontend Agent that handles all client-side implementation, so that UI changes follow existing patterns and maintain consistency.

#### Acceptance Criteria

1. WHEN the Orchestrator delegates a frontend task, THE Frontend_Agent SHALL implement changes using vanilla HTML/CSS/JS matching the existing patterns in `frontend/`
2. THE Frontend_Agent SHALL use the existing `frontend/js/api.js` module for all backend communication with the dynamic `API_BASE` pattern
3. THE Frontend_Agent SHALL integrate sidebar navigation using the existing `frontend/js/menu.js` patterns including permission checks and user-based visibility
4. WHEN creating new pages, THE Frontend_Agent SHALL include the standard sidebar, profile dropdown, and no-cache headers consistent with existing pages
5. THE Frontend_Agent SHALL ensure all UI changes are responsive following the existing mobile-first patterns (edge-tap sidebar, bottom navigation on mobile)
6. WHEN implementation is complete, THE Frontend_Agent SHALL provide a list of all created and modified files to the Orchestrator

### Requirement 5: QA Agent — Testing and Validation

**User Story:** As a developer, I want a QA Agent that validates all changes before they are considered complete, so that regressions and bugs are caught before deployment.

#### Acceptance Criteria

1. WHEN the Orchestrator delegates a QA task, THE QA_Agent SHALL write pytest test cases covering the new or modified functionality
2. THE QA_Agent SHALL validate that all new API endpoints return correct status codes for both success and error cases
3. THE QA_Agent SHALL verify that multi-tenant data isolation is maintained by testing cross-business data access attempts
4. IF any test fails, THEN THE QA_Agent SHALL report the failure details to the Orchestrator with a recommended fix
5. WHEN all tests pass, THE QA_Agent SHALL approve the changes for documentation and deployment
6. THE QA_Agent SHALL verify that no existing functionality is broken by running the full test suite in `commands/testing/`

### Requirement 6: Task Delegation Protocol

**User Story:** As a developer, I want a structured delegation protocol, so that tasks are assigned to the correct agent with clear scope and acceptance criteria.

#### Acceptance Criteria

1. WHEN the CTO_Agent produces an implementation plan, THE Orchestrator SHALL create a Delegation_Payload for each specialized agent containing: task description, files to modify, acceptance criteria, and dependencies on other agents
2. THE Orchestrator SHALL assign UI-related tasks exclusively to the Frontend_Agent and API/database tasks exclusively to the Backend_Agent
3. IF a task has dependencies on another agent's output, THEN THE Orchestrator SHALL enforce sequential execution with the dependency completed first
4. WHEN multiple tasks have no dependencies on each other, THE Orchestrator SHALL delegate them in parallel to reduce session duration
5. THE Orchestrator SHALL track the status of each delegated task (pending, in-progress, completed, failed) throughout the session

### Requirement 7: Documentation Update Protocol

**User Story:** As a developer, I want all documentation to be updated automatically at the end of every session, so that the project history remains accurate and complete.

#### Acceptance Criteria

1. WHEN all delegated tasks are completed and approved by the QA_Agent, THE Orchestrator SHALL update `SYSTEM_UPDATES_DATA_HISTORY_LOGS.md` with a new session entry listing all changes, files modified, and database changes
2. WHEN features are completed, THE Orchestrator SHALL mark the corresponding items in `PROJECT_ROADMAP.md` with `[x]` and update the version number
3. THE Orchestrator SHALL update the `Last Updated` date and `Version` fields at the top of `SYSTEM_UPDATES_DATA_HISTORY_LOGS.md`
4. WHEN creating git commits, THE Orchestrator SHALL follow the branch naming convention from `GIT_BRANCH_GUIDE.md` using the format `<type>/<short-description>`
5. THE Orchestrator SHALL write commit messages that are descriptive and follow the examples in `GIT_BRANCH_GUIDE.md` (e.g., "Feature: add voucher management system")

### Requirement 8: Git Workflow Compliance

**User Story:** As a developer, I want all git operations to follow the established branch guide, so that the repository history remains clean and consistent.

#### Acceptance Criteria

1. WHEN starting work on a new feature, THE Orchestrator SHALL create a branch using the `feature/<short-description>` naming convention
2. WHEN starting work on a bug fix, THE Orchestrator SHALL create a branch using the `fix/<short-description>` naming convention
3. WHEN starting work on an improvement to existing functionality, THE Orchestrator SHALL create a branch using the `update/<short-description>` naming convention
4. THE Orchestrator SHALL always pull the latest changes from main before creating a new branch
5. THE Orchestrator SHALL use `git push -u origin <branch-name>` for the first push of any new branch to set upstream tracking
6. THE Orchestrator SHALL stage specific files rather than using `git add .` to avoid committing unrelated changes

### Requirement 9: Execution Loop Orchestration

**User Story:** As a developer, I want the full execution loop to run in a defined sequence, so that every session follows a predictable and repeatable process.

#### Acceptance Criteria

1. THE Orchestrator SHALL execute the session loop in this order: Context Load → Ideation → Delegation → Development → Testing → Documentation
2. IF the QA_Agent rejects changes, THEN THE Orchestrator SHALL return to the Development phase with the failure details and re-delegate the fix to the appropriate agent
3. WHILE the session is active, THE Orchestrator SHALL maintain a running log of all actions taken, decisions made, and files modified
4. WHEN the user provides a specific task rather than requesting the next roadmap item, THE Orchestrator SHALL skip the Ideation phase and proceed directly to Delegation with the user-specified task
5. IF the user requests a hotfix, THEN THE Orchestrator SHALL use the `hotfix/<description>` branch convention and skip non-essential phases to prioritize speed

### Requirement 10: Error Handling and Recovery

**User Story:** As a developer, I want the workflow to handle errors gracefully, so that failures in one phase do not corrupt the project state.

#### Acceptance Criteria

1. IF a Backend_Agent or Frontend_Agent encounters an unresolvable error, THEN THE Orchestrator SHALL log the error, revert any partial changes, and report the issue to the user
2. IF a database migration fails, THEN THE Backend_Agent SHALL not proceed with dependent code changes and SHALL report the migration failure to the Orchestrator
3. IF the QA_Agent reports test failures after three retry attempts, THEN THE Orchestrator SHALL escalate to the user with a summary of what was attempted and what failed
4. WHEN an error occurs during documentation updates, THE Orchestrator SHALL preserve the existing documentation state and retry the update
5. THE Orchestrator SHALL never leave the repository in a state with uncommitted partial changes at the end of a session

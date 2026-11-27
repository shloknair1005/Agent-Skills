---
name: feature
description: Use this skill whenever the user asks Claude to "add", "implement", "create", "build", or "write" a new feature, or to "enhance", "improve", or "upgrade" an existing feature. This skill is for adding new functionality to a codebase, not for fixing bugs or refactoring existing code. Make sure to understand the user's requirements and the context of the codebase before starting work on a new feature using less tokens and a proper worflow. If the user asks for a feature that is already implemented, politely point out that it already exists and provide instructions for how to use it.
---

# Feature Development

Take a feature request to a working, verified part of the existing application. Isolated code that compiles is not a finished feature. Optimize for correct code on the first pass: fewer tokens spent on rework beats fewer tokens spent on thinking.

## Step 0: Size the work

Classify first, and say the size in one line.

- **Small** (one layer, a few files, no schema or auth change, e.g. add a field, tweak an endpoint): skip the plan and the question round. Do phases 2, 4/5 as needed, and 8 (targeted tests only). Short report.
- **Medium** (spans frontend and backend, or adds an endpoint/table): ask decision questions if needed (see Questions), then run all phases, proceeding after a brief plan.
- **Large or risky** (schema migrations, auth/permissions changes, 8+ files, touches many existing features): ask questions, then **show the plan and wait for approval** before writing code.

## Rules

1. **Inspect narrowly, then edit.** Use grep/glob to find the relevant files. Don't read the whole repo.
2. **Mirror one reference.** Find the most similar existing feature and copy its structure, naming, layering, and test style.
3. **Reuse before creating.** Search for existing components, services, clients, schemas, and utilities. No duplicates.
4. **No new patterns or dependencies** unless the feature cannot work without them.
5. **No fake integration or fake data.** The real flow must work. Mocks only in tests.
6. **Preserve existing behavior.** No unrelated refactors. Never weaken or delete an existing test to get green.
7. **Verify, don't assume.** Never say "this should work." Run it.

## Code quality (avoid AI slop)

- Minimal diff: change only what the feature needs. No drive-by reformatting or renames.
- No speculative abstractions, config options, flags, or generic helpers for a single use.
- No dead code, commented-out code, placeholder TODOs, or stubbed functions.
- Comments only where the *why* is non-obvious. Don't narrate what the code does.
- Handle specific, expected errors. No blanket try/except or catch-and-ignore; no swallowed failures.
- Match existing naming, types, and error/response formats exactly.
- Validate at system boundaries (user input, external APIs), not redundantly everywhere.
- Before finishing, review your own diff once and remove anything above that slipped in.

## Questions (minimize rework)

Ask only about decisions that would cause **rework if guessed wrong**: data model shape, permissions/who can do what, behavior on edge cases, scope boundaries, UX choices with real alternatives.

- Search the codebase first. Never ask what the code can answer.
- Ask **once, batched**, up to ~4 questions, each with a recommended default so the user can reply "defaults" or just a few words.
- Don't ask about naming, styling, file placement, or anything the existing patterns decide.
- For minor choices, decide, and list the assumptions in one line in the plan or report.
- After the round, don't interrupt again unless you hit something that invalidates the plan.

## Phase 1: Understand

Work out the problem, user, flow, inputs/outputs, which existing features it touches, and whether it needs auth, DB changes, endpoints, or UI. Read `CLAUDE.md`/`README`/`CONTRIBUTING` if present; they override this skill and give the real test, lint, and build commands.

## Phase 2: Inspect

Identify only what the feature touches: frameworks, ORM/DB, auth, API and routing structure, service/data-access layers, validation and error conventions, test setup. Read the reference feature and the specific files you'll modify. Don't re-read files you've already seen unless they changed.

## Phase 3: Plan

Brief and concrete: files to create/modify, models/schemas/endpoints, UI pieces and states, routes and nav, which existing features connect, and which tests to write. Include one-line assumptions. For Large work, present it and wait for approval.

## Phase 4: Backend (if needed)

- Follow existing layering; business logic in the service layer if one exists.
- Change models only when necessary; every schema change gets a migration.
- Add schemas, validation, auth and authorization checks, error handling, and logging where the project does so.
- Never bypass existing auth. Never expose sensitive fields.

## Phase 5: Frontend (if needed)

- Reuse existing components and the existing API client; follow UI conventions.
- Implement loading, empty, error, and success states, input validation, and auth-state handling.
- No unnecessary global state.

## Phase 6: Routing

Verify, don't assume: the frontend route renders the right component, params work, protected routes are protected, nav links exist; the backend route is registered with the right method, middleware, and validation; and the frontend calls the correct endpoint.

## Phase 7: Integrate

Identify existing features that should interact with the new one (APIs, DB relationships, users, permissions, notifications, dashboards, search, workflows, jobs). Use existing relationships, not disconnected copies of data.

## Phase 8: Test (cheap first, broad once)

1. Write tests for the new behavior following existing test style: unit for logic, API tests for success, invalid input, auth/authorization failures, missing and duplicate resources.
2. Run **only the new and directly related tests** while iterating.
3. When those pass, run formatter, linter, type checker, and build.
4. Run the **full existing suite once** at the end for regressions (auth, existing routes/APIs, migrations, shared components).
5. Exercise the real user flow end to end (UI or API through DB and back, plus related features). Cover the happy path and the key failure paths.

Keep command output short (filter, tail, or quiet flags); don't dump full logs into context.

## Phase 9: Debug (bounded)

Find the actual failure, trace the data flow to the root cause, fix it, re-run the failing test, then related tests. Don't patch symptoms or edit a test just to pass it unless the test is wrong.

**After 3 failed attempts on the same issue, stop.** Summarize what you tried and what you've learned, and ask the user how to proceed.

## Safety

- Run migrations and tests only against a dev/test database, never production. Check the connection target before running anything that writes.
- Never commit or print secrets, tokens, or `.env` values.
- Ask before destructive commands: drop/truncate/reset, `rm -rf`, force-push, `git reset --hard`, or deleting data.
- Don't commit or push unless asked.
- If a required check can't run (no test setup, no credentials, no running environment), say so rather than claiming it passed.

## Final verification

Confirm the chain works wherever relevant: UI → route → API request → backend route → auth → validation → business logic → DB → response → UI update → related features.

Done means: requirement implemented, existing architecture respected, auth and validation handled, UI states covered, routes connected, existing features integrated, new and existing tests pass, build/lint/types pass, no obvious regressions.

## Final report (short)

- **Implemented / Modified:** what was added, and key existing code changed.
- **Integration:** how it connects to existing features.
- **Testing:** what ran and the results; anything not verified.
- **Assumptions and issues:** decisions made without asking, and known limitations.
- **Files changed:** the important ones.

Declare complete only if the done criteria are met; otherwise state what remains.
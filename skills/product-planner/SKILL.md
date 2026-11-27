---
name: product-planner
description: Interviews the user until a product idea is fully understood, then writes an end-to-end execution plan as Obsidian notes, one self-contained .md file per execution phase, so the `feature` or `fullstack-agent-crew` skill can implement each phase with minimal tokens. Asks and confirms everything (assumes nothing), pushes back with better alternatives, tracks every user constraint, and documents research in the project vault via obsidian-vault-keeper. Make sure to use this skill whenever the user wants to plan, scope, spec, or break down a product, app, feature set, enhancement, or migration before building it; says "I have an idea", "help me think this through", "let's plan", "write a PRD/spec", "break this into phases"; or describes a large, ambiguous, or multi-layer request (DB, backend, UI) with no plan yet, even without saying "plan". Do NOT use to implement code (use `feature` or `fullstack-agent-crew`), fix bugs, refactor, or make a small, clear, single-layer change; say so in one line and hand off.
allowed-tools: Read, Grep, Glob, Bash, Write, Edit, AskUserQuestion
compatibility: Built for Claude Code. Requires the obsidian-vault-keeper skill (all notes go through it). scripts/plan_lint.py needs Python 3 (standard library only). Output is meant for the `feature` and `fullstack-agent-crew` skills.
metadata:
  version: 1.0.0
  category: engineering-workflow
---

# Product Planner

Turn a rough idea into a plan that implementation sessions can run without exploring, guessing, or asking. Interview the user until the product is fully understood. Record the research in the project's Obsidian vault. Write one self-contained note per execution phase. Implementation then runs through the `feature` or `fullstack-agent-crew` skill, one phase per fresh session.

**Why the plan has this shape.** Implementation tokens go to three things: re-reading the repo, questions asked mid-build, and rework after a wrong guess. This skill pays those costs once, up front, in a cheap read-only session, and freezes the answers into phase files. Every rule below serves that goal.

## Standing rules

1. **Assume nothing about the product.** Every product decision (users, scope, behavior, data, permissions, edge cases, priorities) is asked and confirmed. A recommended default is only a suggestion. It becomes a decision when the user picks it. Silence is not consent: an unanswered question stays open and you ask it again.
2. **Verified repo facts are not assumptions.** What you read in the code (stack, layers, auth pattern, test commands) is recorded with its file path and shown to the user once for confirmation. Do not ask the user what the code can answer. Do flag it when the code contradicts what the user believes.
3. **Constraints are law.** Keep the constraint ledger (see below) and re-read it at every checkpoint.
4. **Push back with evidence.** When you see a simpler, cheaper, safer, or already-existing alternative, say so before moving on. Follow `references/question-guide.md`.
5. **Read-only toward the repo.** Never edit source files, run migrations, or run anything that writes outside the vault. The only files you write are vault notes.
6. **Vault discipline.** Create and update every note through the `obsidian-vault-keeper` skill: one vault per project, simplified technical English (its Step 8) for note bodies and for your explanations, a log entry for every change (its Step 9), and the index kept current (its Step 3). Write notes once per round, not once per message, so the log stays useful and cheap.
7. **No phase files before both gates pass.** Gate 1 is the user confirming the Product Brief. Gate 2 is the user approving the Plan Overview.

## Constraint ledger

The ledger is `04-Reference/Constraints.md`. It is a table: `ID | Statement | Source | Status | Date`. Status is `confirmed`, `proposed`, or `dropped`.

- **S-nn standing constraints.** Seed these at Stage 0:
  - S-01: Implementation runs through the `feature` skill or the `fullstack-agent-crew` skill, one phase per session.
  - S-02: Implementation must use as few tokens as possible: no repo scans, no question rounds, no re-reading of research.
  - S-03: Every execution phase is a separate, self-contained .md file in the vault.
  - S-04: Nothing is assumed. The user confirmed every product decision.
- **C-nn user constraints.** Add one whenever the user states a limit or preference: "must", "can't", "don't", "only", "no X", "we use", "by <date>", a budget, a team limit, a compliance rule, a preferred tool. Quote the user in Source. Add it in the same round you hear it, with status `confirmed` if stated as a rule or `proposed` if you inferred it (then ask).
- **R-nn repo constraints.** Facts from the code that the plan must respect (for example "migrations are raw SQL in `db/migrations/`"). Source is a file path.

Re-read the ledger before: each question round, each pushback, the Plan Overview, and each phase file. If new information conflicts with a constraint, stop and show the conflict to the user right away. Only the user can drop a constraint. Mark it `dropped` with the date. Never delete a row.

## Workflow

### Stage 0: Triage and set up

1. **Triage size.** If the request is small, clear, and single-layer, say so in one line, point to the `feature` skill, and ask whether the user still wants a full plan. Follow the answer.
2. **Confirm the project slug** with the user (recommend the repo name). Then resolve or create the vault with `obsidian-vault-keeper` Steps 0 to 1. If the vault exists, resume (see "Resuming").
3. **Add the planner folder** `06-Execution/` to the vault. This extends the vault's standard folders; create only the folders you need.
4. **Create the control notes** from `references/vault-notes.md`: `05-Meta/Planning Status.md`, `04-Reference/Constraints.md` (seeded with S-01 to S-04), and `00-Inbox/Open Questions.md`.
5. **Check you can write.** If the vault skill is missing or the vault folder is not writable, tell the user and ask how to proceed (for example, allow the folder with `/add-dir`, or choose another location). Do not choose silently.
6. **Pick the question channel.** Use the `AskUserQuestion` tool when available (up to 4 questions per call, 2 to 4 options each). Otherwise ask numbered questions in chat with lettered options.

### Stage 1: Intake and repo recon

1. Let the user explain the idea in their own words first. Do not open with a questionnaire. If they already described it, do not ask again.
2. Extract every constraint they state into the ledger.
3. If a repo exists, do a narrow recon. Find: framework and language, layering (routes, services, data access), ORM or raw SQL, migration style and location, auth and roles, frontend stack and design system, test, lint, type-check, and build commands (read `CLAUDE.md`, `README`, `CONTRIBUTING`, CI config), and the features closest to the idea. Use grep and glob. Do not read the whole repo.
4. Record the result in `04-Reference/Repo Conventions.md` and `01-Architecture/` notes. Add R-nn constraints. Check whether the requested feature already exists; if it does, tell the user and ask what they want to do.
5. If there is no repo yet, skip the recon. Stack questions become normal discovery questions.

### Stage 2: Discovery rounds (loop)

Goal: every item in `references/discovery-checklist.md` is `confirmed` or `na-confirmed`, and `Open Questions.md` has no open items.

Each round:

1. Re-read the ledger and `Planning Status.md`.
2. Pick the next 4 or fewer unconfirmed items. Go in order: problem, users, scope, behavior, data, access, integrations, quality, then delivery and operations. Do not ask technical questions before the product is clear.
3. Ground each question in the repo when you can ("The app has roles `admin` and `member` in `auth/roles.py`. Can `member` do X?").
4. Add a **pushback** block first if you see a better alternative.
5. Ask the batched questions. Each question has 2 to 4 options, one marked as recommended, and a one-line reason that says what would be reworked if the answer is wrong.
6. After the answers, restate what changed in 2 or 3 lines. Then write the notes for the round in one batch: the `Discovery - <Area>` notes, decision notes, ledger rows, `Open Questions`, `Planning Status`. Log each change.
7. Show coverage in one line: "Confirmed 14 of 51. Next: users and scope."

Read `references/question-guide.md` before the first round. It covers question format, pushback format, and how to handle "I don't know", "you decide", vague answers, and scope growth.

**Batch the small confirmations.** Items that look not applicable, and repo facts you verified, go in one confirmation question each ("I plan to treat these as out of scope: A, B, C. Confirm?"). The user answers once. Nothing is skipped silently, and the user is not asked 20 times.

**Never stop early.** Keep going until the checklist is complete. If the user wants to move faster, offer to list all remaining recommended defaults at once for a single confirm. Record each one as a `delegated` decision, so it is still confirmed.

### Stage 3: Gate 1 (Product Brief)

1. Write `04-Reference/Product Brief.md` (template in `references/vault-notes.md`). It is the synthesis of all `Discovery` notes. Link to them; do not copy them.
2. Show the user a summary in 25 lines or fewer: problem, users, scope in and out, journeys, key decisions, constraint IDs, verified repo facts, risks.
3. Ask: "Is this correct and complete? List corrections." Go back to Stage 2 for any correction.
4. The gate passes only on an explicit yes. Record the date in the brief.

### Stage 4: Gate 2 (Plan Overview)

Write `06-Execution/Plan Overview.md` and show the phase table. Use these rules.

**Phase rules**
- Each phase is a **vertical slice** that delivers working, verifiable behavior through the real flow. Code that only compiles is not a phase. The only exception is a foundation phase when a shared schema or config is unavoidable; it must still be verifiable (the migration applies, tests pass).
- Each phase fits **one implementation session**. For the `feature` route, aim for 8 files or fewer. For the `fullstack-agent-crew` route, aim for about 15 files across layers. If a phase is larger, split it.
- Order by dependency. Put risky or unknown work early. Every phase leaves the app working and can be reverted alone. Prefer additive migrations.
- Phase files are numbered `Phase 01 - <Name>.md`, `Phase 02 - ...`.

**Route rules** (the same size classes as the `feature` skill's Step 0)

| Phase shape | Route | Size |
|---|---|---|
| One layer, no schema or auth change | `feature` | small |
| Frontend and backend together, or one new endpoint or table, tightly coupled | `feature` | medium |
| New schema, API, and UI in one phase, with enough work in each layer that parallel agents save time | `fullstack-agent-crew` | medium or large |
| Auth, permissions, or migrations on existing data | either route | large (flag it) |

Never use the crew route for a single-layer phase. The crew skill needs the `Task` tool; each crew phase says what to do if it is missing.

The Plan Overview also holds: the constraint traceability table (every ID mapped to the phases that honor it; an unmapped constraint blocks the gate), the confirmed out-of-scope list, product-level done criteria, and risks.

Ask the user to approve the order, the phase sizes, and the cut lines. Push back if the scope is too big for a first release. The gate passes only on an explicit approval.

### Stage 5: Write the phase files

For each phase, re-read the ledger and the related decisions. Then write `06-Execution/Phase NN - <Name>.md` from `references/phase-template.md`.

A phase file must:
- be **self-contained**: an implementation session reads this one file plus the files it lists, and nothing else;
- carry the **verbatim text** of each applicable constraint, the decisions already made, the repo facts it needs (including the reference feature to mirror and the exact test commands), and the exact file paths (verify with grep that paths to modify exist and that the folders for new files exist);
- link to research notes with `[[wikilinks]]` marked optional, never copy them;
- contain **no** `TBD`, `TODO`, "decide later", or unconfirmed choice. If something is unknown, you are not done with Stage 2;
- stay near 150 lines and use the vault skill's writing style (short, active, one action per step);
- for the crew route, include a **Contract draft** (schema and endpoints, ready to copy to `agents/contract.md`) and a **File ownership** table with no overlap.

Write all phase files, then update the Plan Overview links and the vault index.

### Stage 6: Lint and hand off

1. Run `python3 <skill-folder>/scripts/plan_lint.py <vault-path>`. Fix every error and re-run until it passes. It checks required sections, valid frontmatter, dependency order, constraint coverage, broken wikilinks, banned placeholder words, open questions, unconfirmed constraints, and gates still marked "not passed".
2. Send a final message of 15 lines or fewer: the vault path, the phase table (route, size), the first start prompt, and the open risks. Tell the user to run each phase in a fresh session. The start prompt is in the `Run this phase` section of each phase file.
3. Set `stage: done` in `Planning Status.md`.

## How the phase files cut implementation tokens

| Where tokens go today | What the phase file provides |
|---|---|
| `feature` Step 0 sizing and question round | Size and route are set. All decisions are confirmed. The note says not to ask again. |
| `feature` Phases 1 to 3 (understand, inspect, plan) | Scope, repo facts, reference feature, file list, and tasks are written. The plan is already approved. |
| `feature` Phase 8 (test) | Targeted and full test commands, and acceptance criteria, are written. |
| `fullstack-agent-crew` Step 0 (scope) | Scope and repo conventions are in the note, so the default stack assumptions never apply. |
| `fullstack-agent-crew` Steps 1 and 2 (schema, contract) | The Contract draft is ready. The DB agent implements the draft and does not redesign it. |
| `fullstack-agent-crew` Step 3 (file ownership) | The File ownership table is written. |

## Resuming and changing the plan

- **Resume.** If the vault exists, run the vault skill's check for edits made outside the skill. Read `Index.md`, `Planning Status.md`, `Constraints.md`, and `Open Questions.md`. Continue from the recorded stage. Do not re-ask a confirmed item.
- **Changed requirement.** Treat it as a new Stage 2 item. Mark old notes as superseded (vault skill Step 5), update the affected phase files only, re-run the lint, and show the user what changed.
- **Drift after implementation.** If a finished phase changed the repo in a way that affects later phases, update those phase files before the next session starts. Check them against the repo first.

## Files in this skill

- `references/discovery-checklist.md`: the coverage list for Stage 2. Read it at Stage 1.
- `references/question-guide.md`: questions, pushback, and edge-case answers. Read it before the first round.
- `references/vault-notes.md`: note map and templates for the control notes, brief, decisions, and overview. Read it at Stage 0.
- `references/phase-template.md`: the phase file template, with the crew additions. Read it at Stage 5.
- `scripts/plan_lint.py`: the pre-handoff check. Run it at Stage 6.

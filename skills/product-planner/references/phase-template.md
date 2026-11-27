# Phase file template

One file per phase: `06-Execution/Phase NN - <Name>.md`. The file is a work order. A fresh implementation session reads this file and the files it lists, and nothing else. Every section is required; `plan_lint.py` checks the headings.

**Contents:** Template · Crew additions · Writing rules · Short example

## Template

```markdown
---
title: Phase <<NN>> - <<Name>>
created: <<YYYY-MM-DD>>
tags: [<<project-slug>>, execution, phase]
phase: <<N>>
status: todo
route: <<feature | fullstack-agent-crew>>
size: <<small | medium | large>>
depends_on: [<<phase numbers, or leave empty>>]
constraints: [<<IDs such as S-01, S-02, C-03>>]
---

# Phase <<NN>> - <<Name>>

## Goal
<<One sentence: what a user can do after this phase.>>

## Run this phase
1. Start a new session in the repo at `<<repo path>>`.
2. Use the `<<route>>` skill. Size: <<size>>.
3. The user approved this plan on <<date>>. Do not ask the user again. Do not show a plan and wait.
4. Read only this note and the files in "Files". Do not scan the repository.
5. Do not read other vault notes unless a task here is unclear.
6. Keep command output short.

Start prompt:
> Implement `<<vault path>>/06-Execution/Phase <<NN>> - <<Name>>.md` with the `<<route>>` skill. The plan is approved. Follow "Run this phase".

## Constraints that apply
- <<ID>>: <<verbatim statement>>

## Already decided
- <<Decision in one line>>. Detail (optional): [[Decision - <<Topic>>]]

## Scope
- **In:** <<list>>
- **Out:** <<list, from confirmed non-goals>>

## Repo facts
- **Stack:** <<language, framework, DB>>
- **Mirror this feature:** `<<path>>` (<<what to copy: layering, naming, test style>>)
- **Migrations:** <<style and location>>
- **Auth pattern:** <<how roles are checked>>
- **Test (targeted):** `<<command>>`
- **Test (full):** `<<command>>`
- **Lint, types, build:** `<<commands>>`

## Files
- **Create:** `<<path>>`: <<purpose>>
- **Modify:** `<<path>>`: <<what changes>>
- **Do not touch:** <<paths or areas>>

## Tasks
1. <<One action. Name the file and the thing to add.>>
2. <<...>>

## Acceptance criteria
- [ ] <<Check that a person or a test can run.>>
- [ ] <<Failure path: for example "Invalid input returns 422 and no row is saved".>>

## Tests
- **Write:** <<test files and the cases: success, invalid input, auth failure, missing, duplicate>>
- **Run:** targeted tests first. Then lint, types, and build. Then the full suite once.

## Stop and ask only if
- The same failure repeats 3 times.
- A task here conflicts with a constraint above.
- A file in "Files" is missing or has changed so that a task cannot be done.

## Handoff
When all acceptance criteria pass:
1. Set `status: done` in the frontmatter of this note.
2. Add a completion note of 3 lines or fewer below.

The next phase needs: <<names, tables, endpoints, or flags that exist after this phase>>.

## Completion note
```

## Crew additions

For `route: fullstack-agent-crew`, change step 2 of "Run this phase" and add the sections below.

Replace step 2 with:
> 2. Use the `fullstack-agent-crew` skill. Size: <<size>>. Skip its Step 0 scoping: scope and repo facts are in this note. If the `Task` tool is not available, tell the user and run the Tasks below in order with the `feature` skill.

Add after the "Run this phase" list:
> 7. The DB agent implements the schema in "Contract draft". It does not redesign it. It reports only gaps.
> 8. Copy "Contract draft" to `agents/contract.md` (replace the file from an earlier phase). Skip the crew skill's Step 2 drafting.

Add these sections after "Files":

```markdown
## Contract draft
Working copy goes to `agents/contract.md`.

### Existing schema this phase uses
<<Only the tables and columns that matter.>>

### New schema
<<Tables, columns, types, keys, constraints, defaults, enums.>>

### Endpoints
| Method and path | Owner | Request | Response | Status codes |
|---|---|---|---|---|
| POST /<<path>> | backend | <<fields>> | <<shape>> | 201, 422, 403 |

### Shared types
<<Names and shapes the frontend must match.>>

## File ownership
| Agent | May edit | Must not edit |
|---|---|---|
| DB | `<<migration path>>` | all other code |
| Backend | `<<paths>>` | migrations, middleware, frontend |
| Middleware | `<<paths>>` | migrations, backend logic, frontend |
| Frontend | `<<paths>>` | migrations, backend, middleware |
```

Rules for ownership: no file appears in two rows. If two agents need one file (for example a shared `routes.py`), give it to one agent and write the other agent's addition in "Tasks" as a snippet for the coordinator to merge.

Group "Tasks" by agent for this route: DB, Backend, Middleware, Frontend, Integration. The Integration tasks are for the coordinator: register routes, merge shared snippets, trace one request from the database to the UI.

If the codebase has no separate middleware layer, write "No middleware work. Auth checks are in the backend routes." and give the middleware agent no files, so the crew skill does not invent a layer.

## Writing rules

- Use the vault skill's style: short sentences, active voice, one action per step, commands for instructions.
- Put verbatim constraint text in the note. Do not write "see Constraints".
- Use exact paths. Check with grep or ls that each path to modify exists and each folder for a new file exists.
- Use `[[wikilinks]]` only for optional detail. A session must be able to finish without opening them.
- Write acceptance criteria that a test or a command can check. "Works well" is not a criterion.
- No `TBD`, `TODO`, "decide later", or open choice. Stay near 150 lines. If the note grows past 200 lines, split the phase.
- A phase `size` follows the `feature` skill: small (one layer, a few files), medium (frontend and backend, or a new endpoint or table), large (schema migration, auth change, or 8 or more files).

## Short example

```markdown
## Tasks
1. Add the `reports` table migration in `db/migrations/0007_reports.sql`. Match the format of `0006_orders.sql`.
2. Add `get_report(id)` and `create_report(data)` to `services/reports.py`. Use `services/orders.py` as the model.
3. Add `POST /reports` and `GET /reports/<id>` to `routes/reports.py`. Use the `@require_role("admin")` decorator.
4. Register the blueprint in `app.py`.

## Acceptance criteria
- [ ] `POST /reports` as `admin` returns 201 and saves one row.
- [ ] `POST /reports` as `member` returns 403 and saves no row.
- [ ] `POST /reports` with a missing `title` returns 422.
```

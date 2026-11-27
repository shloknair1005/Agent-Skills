# Vault notes for planning

All notes go through the `obsidian-vault-keeper` skill: one vault per project, minimum frontmatter `title`, `created`, `tags: [<project-slug>, <category>]`, `[[wikilinks]]` between notes, simplified technical English for prose, and a log entry for every change. Templates below use `<<field>>` for values to fill in. Replace every one. `plan_lint.py` fails on a leftover `<<field>>`.

**Contents:** Note map · Planning Status · Constraints · Open Questions · Discovery note · Decision note · Repo Conventions · Product Brief · Plan Overview

## Note map

| Note | Folder | Purpose | Written |
|---|---|---|---|
| `Planning Status` | `05-Meta/` | Stage, round, checklist coverage | Stage 0, every round |
| `Constraints` | `04-Reference/` | The constraint ledger | Stage 0, every round |
| `Open Questions` | `00-Inbox/` | Unanswered questions | Stage 0, every round |
| `Discovery - <Area>` | `04-Reference/` | Every question, option, and answer for one area (A to L) | Created on first answer in the area |
| `Decision - <Topic>` | `02-Decisions/` | A real choice, or any pushback: options, trade-offs, decider | When decided |
| `Repo Conventions` | `04-Reference/` | Verified repo facts with file paths | Stage 1 |
| `Architecture - <Component>` | `01-Architecture/` | Existing and planned structure, data model, flows | Stage 1 and 2 |
| `Glossary` | `04-Reference/` | Product terms, one definition each | As terms appear |
| `Product Brief` | `04-Reference/` | Synthesis for Gate 1 | Stage 3 |
| `Plan Overview` | `06-Execution/` | Phases, routes, traceability for Gate 2 | Stage 4 |
| `Phase NN - <Name>` | `06-Execution/` | One work order per phase | Stage 5 |

Search the vault before you create a note (vault skill Step 5). Never keep one concept in two notes.

## Planning Status

```markdown
---
title: Planning Status
created: <<YYYY-MM-DD>>
tags: [<<project-slug>>, planning, meta]
stage: intake
round: 0
---

# Planning Status

Stages: intake, discovery, brief-gate, plan-gate, phases, done.

## Coverage
Item IDs come from the discovery checklist. Move an ID to one line only.

confirmed:
asked:
open: A1 A2 A3 A4 A5 B1 B2 B3 B4 C1 C2 C3 C4 D1 D2 D3 D4 D5 D6 E1 E2 E3 E4 E5 F1 F2 F3 F4 G1 G2 G3 G4 H1 H2 H3 H4 I1 I2 I3 I4 J1 J2 J3 J4 J5 K1 K2 K3 L1 L2 L3
na-confirmed:

## Gates
- Gate 1 (Product Brief): not passed
- Gate 2 (Plan Overview): not passed
```

When all IDs are in `confirmed` or `na-confirmed`, the `open:` and `asked:` lines are empty. Set `stage` as you move. Update the gate lines with the date when a gate passes.

## Constraints

```markdown
---
title: Constraints
created: <<YYYY-MM-DD>>
tags: [<<project-slug>>, reference, constraints]
---

# Constraints

Only the user can drop a constraint. Never delete a row.

| ID | Statement | Source | Status | Date |
|---|---|---|---|---|
| S-01 | Implementation runs through the `feature` skill or the `fullstack-agent-crew` skill, one phase per session. | Planner standing rule | confirmed | <<date>> |
| S-02 | Implementation must use as few tokens as possible: no repo scans, no question rounds, no re-reading of research. | User request | confirmed | <<date>> |
| S-03 | Every execution phase is a separate, self-contained .md file in the vault. | User request | confirmed | <<date>> |
| S-04 | Nothing is assumed. The user confirmed every product decision. | User request | confirmed | <<date>> |
```

## Open Questions

```markdown
---
title: Open Questions
created: <<YYYY-MM-DD>>
tags: [<<project-slug>>, planning, inbox]
---

# Open Questions

- [ ] Q-01 <<Question>>. Needed to decide: <<what is missing>>. Blocks: <<checklist IDs>>.
- [x] Q-00 <<Resolved question>>. Answer: <<answer>>. See [[Discovery - <<Area>>]].
```

Keep resolved items for the record. Gate 1 needs zero `- [ ]` lines.

## Discovery note

One per area. Add a section for each question.

```markdown
---
title: Discovery - <<Area name>>
created: <<YYYY-MM-DD>>
tags: [<<project-slug>>, reference, discovery]
---

# Discovery - <<Area name>>

## <<ID>> <<Item>>
- **Asked:** <<date>>, round <<n>>
- **Question:** <<text>>
- **Options:** <<A, B, C>>
- **Answer:** <<what the user chose or wrote, quoted when short>>
- **Status:** confirmed | na-confirmed | delegated
- **Notes:** <<context, repo evidence, links such as [[Decision - Topic]]>>
```

When an answer changes, add a dated section and mark the old one `> [!note] Superseded on <<date>>`.

## Decision note

Use the vault skill's decision template if its `references/note-templates.md` exists. Otherwise use this one.

```markdown
---
title: Decision - <<Topic>>
created: <<YYYY-MM-DD>>
tags: [<<project-slug>>, decision]
---

# Decision - <<Topic>>

- **Context:** <<why this came up>>
- **Options:**
  1. <<Option>>: <<trade-offs>>
  2. <<Option>>: <<trade-offs>>
- **Pushback made:** yes | no. <<one line>>
- **Decision:** <<chosen option>>
- **Decided by:** user | delegated to Claude
- **Constraints touched:** <<IDs>>
- **Effects on phases:** <<phase numbers or "not yet known">>
```

## Repo Conventions

```markdown
---
title: Repo Conventions
created: <<YYYY-MM-DD>>
tags: [<<project-slug>>, reference, repo]
---

# Repo Conventions

Verified by reading the repo on <<date>>. The user confirmed these facts on <<date>>.

| Area | Fact | Evidence (path) |
|---|---|---|
| Language and framework | <<...>> | <<path>> |
| Layering | <<routes, services, data access>> | <<path>> |
| Database and ORM | <<...>> | <<path>> |
| Migrations | <<style and location>> | <<path>> |
| Auth and roles | <<pattern>> | <<path>> |
| Frontend stack and design system | <<...>> | <<path>> |
| Test command (targeted) | `<<command>>` | <<path>> |
| Test command (full) | `<<command>>` | <<path>> |
| Lint, type check, build | `<<commands>>` | <<path>> |
| Closest existing features | <<names>> | <<path>> |
| Fragile areas | <<...>> | <<path>> |
```

## Product Brief

```markdown
---
title: Product Brief
created: <<YYYY-MM-DD>>
tags: [<<project-slug>>, reference, brief]
confirmed_on: <<date of Gate 1>>
---

# Product Brief

## Problem and users
<<Short text. Link [[Discovery - Problem and value]] and [[Discovery - Users]].>>

## Success measures
<<From A3.>>

## Scope
- **In (first release):** <<list>>
- **Out (confirmed):** <<list>>
- **Later:** <<list>>

## Journeys
<<One line per journey. Link the Discovery note.>>

## Key rules, data, and access
<<Short. Link the Discovery notes.>>

## Constraints
<<List the IDs. Link [[Constraints]].>>

## Verified repo facts
<<Link [[Repo Conventions]].>>

## Decisions
<<Links to every [[Decision - ...]] note. List delegated decisions separately.>>

## Risks
<<From L1 to L3.>>
```

## Plan Overview

```markdown
---
title: Plan Overview
created: <<YYYY-MM-DD>>
tags: [<<project-slug>>, execution, plan]
approved_on: <<date of Gate 2>>
---

# Plan Overview

Goal: <<one sentence>>. Brief: [[Product Brief]].

## Phases

| # | Phase | Route | Size | Depends on | Outcome |
|---|---|---|---|---|---|
| 1 | [[Phase 01 - <<Name>>]] | feature | small | none | <<what works after it>> |

## Order and reasons
<<Why this order. Where the risk is.>>

## Constraint traceability

| ID | Statement | Honored in phases |
|---|---|---|
| S-01 | <<text>> | all |
| C-01 | <<text>> | 1, 3 |

## Out of scope (confirmed)
<<List.>>

## Done for the whole product
<<From K3.>>

## Risks
<<Risk and the phase that reduces it.>>

## How to run
Run each phase in a fresh session. Open the phase note. Follow its `Run this phase` section.
```

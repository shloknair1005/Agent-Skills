# Discovery checklist

The coverage list for Stage 2. Each item must end as `confirmed` or `na-confirmed`.
Track status in `05-Meta/Planning Status.md` (one line per status, IDs only).
Record the answers in `04-Reference/Discovery - <Area>.md` (one note per area).

**Contents:** A Problem and value · B Users · C Scope · D Behavior · E Data · F Access and security · G Integrations · H Non-functional · I UX · J Delivery · K Quality · L Risks

**N/A rule.** Do not skip an item because it looks irrelevant. Collect the doubtful items and ask one batched question: "I plan to treat A4, H3, I4 as not applicable. Confirm, or tell me which one matters." Record the confirmed ones as `na-confirmed`.

**Add items freely.** If the idea needs a question that is not listed, add an ID (for example `D7`) to the tracker and ask it.

| ID | Must be known |
|---|---|
| **A** | **Problem and value** |
| A1 | The problem in the user's words, and who feels it |
| A2 | Why now: what triggered the request |
| A3 | Success measure: numbers or observable results, and how they are measured |
| A4 | What happens if this is not built (value check) |
| A5 | How people solve it today, and any existing feature in the repo that overlaps |
| **B** | **Users** |
| B1 | User types who use the feature |
| B2 | Each type's goal, context (device, place), and how often they use it |
| B3 | Who administers or operates it |
| B4 | Volume: number of users, size of data, expected growth |
| **C** | **Scope** |
| C1 | What is in the first release (MVP) |
| C2 | What is out of scope (non-goals) |
| C3 | Later ideas (parking lot) |
| C4 | Priority order if something must be cut |
| **D** | **Behavior** |
| D1 | Each user journey, step by step (happy path) |
| D2 | Failure and edge paths per journey: invalid input, duplicates, concurrent edits, partial failure |
| D3 | Business rules and calculations |
| D4 | Lifecycle of each core object: create, edit, archive, delete, restore |
| D5 | Notifications, emails, and events that the feature triggers |
| D6 | Search, filter, sort, paging, import, and export for any list of data |
| **E** | **Data** |
| E1 | Core entities and how they relate |
| E2 | Fields: type, required or optional, unique, allowed values |
| E3 | Existing data: migration or backfill, volume, allowed downtime |
| E4 | Retention and deletion (soft or hard), audit trail |
| E5 | Source of truth, and links to existing tables |
| **F** | **Access and security** |
| F1 | Role and permission matrix: who can create, read, update, delete |
| F2 | Authentication method and session rules |
| F3 | Sensitive data (personal data, secrets, payments) and compliance rules |
| F4 | Abuse cases: rate limits, input validation, tenant isolation |
| **G** | **Integrations** |
| G1 | Existing features that must change or connect |
| G2 | Third-party services: which, how they authenticate, limits, cost, behavior on failure |
| G3 | Build, buy, or reuse for each significant component |
| G4 | Backward compatibility: existing API clients, URLs, stored data |
| **H** | **Non-functional** |
| H1 | Performance targets: latency and throughput |
| H2 | Reliability: availability needs and behavior on failure |
| H3 | Accessibility, supported browsers and devices, languages |
| H4 | Observability: logs, metrics, alerts, analytics events |
| **I** | **UX** (mark `na-confirmed` for API-only work) |
| I1 | Screens or pages, and where users enter them |
| I2 | States on each screen: loading, empty, error, success |
| I3 | Labels and copy, and the design system to reuse |
| I4 | Mobile and responsive needs |
| **J** | **Delivery** |
| J1 | Deadline or milestones, and the reason for them |
| J2 | Who builds, reviews, tests, and accepts |
| J3 | Technical limits: allowed or forbidden dependencies, hosting, budget |
| J4 | Environments: dev and test database, staging, CI |
| J5 | Release method: feature flags, staged rollout, rollback, migration timing |
| **K** | **Quality** |
| K1 | Acceptance criteria that can be checked, per journey |
| K2 | Test expectations: unit, API, end to end, coverage norms |
| K3 | Definition of done for the whole product |
| **L** | **Risks** |
| L1 | The user's biggest unknowns and fears; any spike that is needed |
| L2 | Fragile or risky areas of the repo |
| L3 | Dependencies on people, approvals, or other teams |

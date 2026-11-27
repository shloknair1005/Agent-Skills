---
name: fullstack-agent-crew
description: Spawns four coordinated subagents — a DB agent, a backend agent, a middleware agent, and a frontend agent — to build or modify a full-stack feature in parallel. Use this skill whenever the user asks to build a feature end-to-end, asks to "spawn agents" or "use subagents" for a full-stack task, mentions wanting a DB/backend/middleware/frontend split, or describes work that touches the database schema, API/business logic, an integration or service layer, and the UI in the same request. Also trigger on phrases like "build this across the stack", "parallelize this feature", or "divide this into DB, backend, middleware, and frontend work". Don't use this for single-layer changes (e.g. "fix this CSS bug" or "add an index to this table") — this skill is for multi-layer feature work where parallel agents actually save time.
license: Proprietary
allowed-tools: Task, Bash, Read, Write, Edit, Grep, Glob
compatibility: Requires Claude Code (uses the Task tool to launch parallel subagents). Not usable in Claude.ai chat, which has no subagent support — there the steps below would have to run sequentially in one thread.
metadata:
  version: 1.0.0
  author: DataAstraa
  category: engineering-workflow
---

# Full-Stack Agent Crew

Coordinates four specialized subagents through Claude Code's `Task` tool to build a
full-stack feature: **DB agent → contract → (Backend, Middleware, Frontend agents in
parallel) → integration pass**. The DB and contract steps are deliberately sequential
because everything downstream depends on them; the three implementation agents run
concurrently because a contract makes them independent.

Read `references/agent-prompts.md` for the exact prompt template to give each subagent —
don't paraphrase it from memory, use it verbatim with the bracketed fields filled in.

## When NOT to use this

- Single-layer changes (one file, one concern) — just do it directly, spawning agents adds
  overhead with no payoff.
- The user explicitly wants to pair-program through the change themselves.
- The feature has no meaningful DB or API surface (e.g. pure frontend polish).

If it's borderline, ask the user in one sentence rather than assuming a 4-agent split is
wanted for a small change.

## Step 0 — Scope the feature before spawning anything

Before touching the `Task` tool, get (from the user or from reading the repo) answers to:

1. **What's the feature, in one or two sentences?**
2. **What tables/entities does it touch?** New ones, or existing ones being extended?
3. **What are the read/write operations?** (roughly — the DB agent will nail down exact
   schema, but you need enough to brief it)
4. **Any existing conventions to respect?** Check the repo for these before assuming
   greenfield defaults:
   - Migration style: raw SQL scripts vs. an ORM/migration framework
   - Where shared logic lives (e.g. a single `routes.py`/`services.py` vs. per-feature files)
   - Existing auth/RBAC patterns middleware must plug into
   - Frontend stack: server-rendered templates vs. a JS framework, existing CSS/theme system

Do a quick repo scan (`ls`, `grep` for existing migrations/routes/templates) rather than
asking the user to describe their own codebase to you. Only ask the user about things the
repo can't tell you (business rules, desired UX, priority order).

**Default assumptions if the repo is ambiguous or empty:** Flask backend, PostgreSQL with
hand-written SQL migration scripts (no ORM migration framework), shared route helpers
co-located in a single routes module rather than split into many service files, and a
server-rendered frontend (Jinja templates + vanilla JS/CSS) unless the repo shows a JS
framework already in use. State the assumption to the user in one line and let them correct
it before you spawn agents — don't silently commit to it.

## Step 1 — Spawn the DB agent alone, first

Everything else depends on the schema, so this agent runs solo and must finish before
Step 2. Launch it with a single `Task` call using the DB agent template in
`references/agent-prompts.md`. Its deliverables:

- Final schema (new tables/columns/indexes/constraints)
- Migration script(s), following whatever migration convention Step 0 found
- A short **data contract** written to `agents/contract.md` (create this file if it doesn't
  exist): table names, column names/types, primary/foreign keys, and any constraints other
  agents need to know about (uniqueness, nullability, enums).

Wait for this agent to finish and read its output before proceeding — do not parallelize
this with the others.

## Step 2 — Extend the contract with the API shape

Once the DB agent is done, add to `agents/contract.md` (you write this part, not a
subagent — it's fast and it's the thing that makes parallelization safe):

- Endpoint list: method, path, request body/params, response shape, status codes
- Which layer owns which endpoint (backend vs. middleware — see the role split below)
- Any shared types/interfaces the frontend will need to match

This contract file is the interface boundary. Every agent below reads it and must not
invent a different shape without updating it (and flagging the conflict to you).

## Step 3 — Spawn backend, middleware, and frontend agents together, in parallel

Launch all three with `Task` calls in the **same turn** (multiple tool calls in one
message) so they run concurrently. Use the templates in `references/agent-prompts.md`.
Role split — adjust to the repo's actual architecture, but the default division is:

- **Backend agent**: core business logic and data-access functions/routes that talk to the
  DB per the contract's schema. Owns query/ORM code, validation, core route handlers.
- **Middleware agent**: cross-cutting concerns sitting between backend and frontend/outside
  world — auth/RBAC checks, request/response transformation, rate limiting, logging,
  third-party integrations, or an internal API gateway layer, depending on what the repo
  actually has. If the codebase has no distinct middleware layer, redirect this agent to
  own integration glue and error handling instead of inventing a layer that doesn't exist.
- **Frontend agent**: templates/components, client-side JS, styling, calling the endpoints
  exactly as defined in the contract.

**File ownership must not overlap.** Before spawning, decide (from the repo scan) which
files/directories each agent may touch, and put that in each prompt explicitly. If two
agents would need to edit the same file (e.g. a single `routes.py` per this user's stated
convention of keeping shared helpers there), pick ONE of them to own that file and have the
other propose its addition as a snippet for you to merge, rather than both editing
concurrently.

## Step 4 — Integration pass (you do this, not a subagent)

After all three return:

1. Read each agent's output and diff/check for contract drift — did anyone deviate from
   `agents/contract.md`? If so, reconcile before merging (usually: prefer whichever side is
   harder to change, tell you which one, ask the user only if it's a real design decision).
2. Merge any shared-file additions (e.g. multiple snippets destined for one `routes.py`).
3. Run the project's existing test/lint commands if any exist. Wire the pieces together
   yourself for anything that falls in the gaps between agents (e.g. registering a new
   blueprint, adding an import).
4. Summarize for the user: what each agent built, what you reconciled, what's left to
   verify manually (e.g. "run the migration, then smoke-test the endpoint").

Never tell the user the feature is "done" without having actually traced one request
through DB → backend/middleware → frontend yourself.

## Notes on running agents well

- Give each agent the **contract file path**, not the contract pasted inline — have it read
  the file itself so it always sees the latest version if Step 2 changes.
- Give each agent an explicit **out-of-scope** list (the other three agents' files) so it
  doesn't wander into DB migrations or frontend templates "to be helpful."
- If the feature is small enough that the contract is trivial (one endpoint, one table),
  it's fine to compress Steps 1–2 into a lighter touch — but still write the contract file,
  it's what keeps the parallel agents from colliding.
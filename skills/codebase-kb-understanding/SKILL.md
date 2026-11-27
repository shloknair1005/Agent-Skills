---
name: codebase-kb-understanding
description: Use this skill whenever the user asks Claude to "understand", "get familiar with", "onboard onto", "explore", or "get up to speed on" a codebase or repository — especially at the start of a session before making changes, answering questions, or planning work. Also trigger when the user points Claude at a new project directory without further instructions, or explicitly mentions a knowledge base, KB, docs folder, wiki, or README alongside a codebase. This skill builds understanding by reading the knowledge base first (if one exists) and then verifying/extending that understanding against the actual code, falling back to code-only exploration when no KB is present. Make sure to use this skill before diving into unrelated feature work on an unfamiliar codebase — understanding-first prevents wrong assumptions later.
---

# Codebase + KB Understanding

A repeatable workflow for building an accurate mental model of a codebase, preferring an existing knowledge base (KB) as a starting map and then confirming it against the real code — since KBs are often stale, incomplete, or just plain wrong.

## Workflow

### Step 1: Locate a knowledge base, if one exists

Look for KB material in this rough priority order. Stop as soon as you have a reasonable candidate — don't exhaustively search every possible location if you find a strong match early.

- Root-level docs: `README.md`, `ARCHITECTURE.md`, `CONTRIBUTING.md`, `docs/`, `documentation/`, `kb/`, `knowledge-base/`
- Wiki exports or linked wikis (e.g., a `wiki/` folder, or a link in the README to Confluence/Notion)
- ADRs (Architecture Decision Records), often in `docs/adr/` or `decisions/`
- Design docs, RFCs, or planning docs in `docs/`, `design/`, `rfcs/`
- Any `.md`/`.mdx`/`.rst` files scattered near the root or in a `docs`-like folder
- If the user has told you (in this conversation, in `CLAUDE.md`, or in project config) where their KB lives, trust that over guessing

If nothing turns up after a reasonable look, **treat this as a KB-less codebase** and go straight to Step 3. Don't ask the user "where's your KB?" unless the codebase is large enough that guessing wrong would waste significant time — a quick check for the above patterns is generally enough to decide.

### Step 2: Build an initial mental model from the KB

Read the KB material with the goal of extracting:

- **Purpose** — what the project/service does, who it's for
- **Architecture** — major components, services, layers, how they talk to each other
- **Key entry points** — where execution starts, main modules, important files
- **Conventions** — naming patterns, folder structure rules, coding standards, testing approach
- **Domain vocabulary** — project-specific terms, acronyms, or concepts that won't be obvious from code alone
- **Known gotchas or caveats** — anything explicitly flagged as tricky, deprecated, or in-progress

Treat this as a *hypothesis*, not ground truth. KBs drift from reality — code gets refactored and docs don't get updated. Hold everything you read here loosely until Step 3 confirms it.

### Step 3: Verify and extend against the actual code

Now examine the codebase itself:

- Check that the architecture described in the KB actually matches the directory/module structure you see
- Confirm named entry points, key files, and components actually exist where the KB says they do
- Look for major parts of the codebase that the KB doesn't mention at all — these are gaps to note explicitly
- Spot-check a few core flows (e.g., trace one request/data path end to end) to confirm the KB's description of how things connect is still accurate
- Note anything that contradicts the KB — call these out rather than silently trusting the code or the KB

If there was no KB at all (from Step 1), do this same investigation from scratch, using standard code-exploration signals instead:
- Entry points (`main`, `index`, `app`, framework-specific bootstrap files)
- Package/dependency manifests (`package.json`, `pyproject.toml`, `go.mod`, etc.) to infer stack and structure
- Directory structure and naming conventions
- Tests, since they often document expected behavior better than comments do
- Any inline comments or docstrings that explain intent, not just mechanics

### Step 4: Synthesize and report back

Produce a concise summary (don't just dump raw findings) covering:

1. **What the project does** (1–3 sentences)
2. **Architecture overview** — major components and how they relate (a short list or a simple diagram if it helps)
3. **Where the KB and code agreed** — brief, no need to belabor this
4. **Where the KB and code diverged, or where the KB was silent** — this is usually the most valuable part; be specific about what's stale/missing
5. **What you'd want to confirm with the user** if anything is still ambiguous after looking at both sources

Keep this proportional to the codebase's size — a small service doesn't need an exhaustive report; a large monorepo may warrant more structure (e.g., grouped by service/package).

## Notes

- Don't modify any files during this process — this is a read/understand workflow, not a refactor.
- If the KB is large, skim for structure first (headings, table of contents) rather than reading every file in full before starting Step 3.
- If time/context is limited, prioritize breadth (touch every major component) over depth (fully tracing one component) — a shallow-but-complete map is usually more useful than a deep dive into one corner.

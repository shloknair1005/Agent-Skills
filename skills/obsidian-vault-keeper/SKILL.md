---
name: obsidian-vault-keeper
description: Creates, organizes, and updates per-project Obsidian knowledge-base vaults — plain markdown notes with frontmatter and [[wikilinks]] that Obsidian reads directly. Use this skill whenever the user asks to document something "in Obsidian" or "in the vault", asks to create/update a knowledge base or notes for a project, says things like "note this down", "log this decision", "write this up for later", "add this to my notes", or when starting a new project that doesn't have a vault yet. Also trigger when the user asks to find, search, or link existing notes. Don't use this for one-off scratch notes the user explicitly says are throwaway, and don't use it for code comments or docstrings — those stay in the codebase, not the vault.
license: Proprietary
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
compatibility: Requires Claude Code (or another environment with local filesystem access). Obsidian itself isn't required to be running — vaults are just folders of markdown files with an .obsidian/ config folder; Obsidian only needs to be open if the user wants to see the graph view or use Obsidian-specific plugins.
metadata:
  version: 1.0.0
  author: Shlok
  category: knowledge-management
---

# Obsidian Vault Keeper

Manages Obsidian vaults as the durable knowledge base for each project. The core rule,
non-negotiable: **one vault per project.** Never merge two projects' notes into one vault,
and never scatter one project's notes across several vaults.

## Step 0 — Locate or establish the vault base directory

Vaults live under a single base directory so they're easy to find and so Obsidian can be
pointed at all of them. On first use in an environment, check in this order:

1. Look for an existing base directory: `~/Obsidian/`, `~/obsidian-vaults/`, or
   `~/Documents/Obsidian/` (check all three with `ls`).
2. If one exists and already has vault-looking subfolders (a folder containing an
   `.obsidian/` directory, or at least markdown files), that's the base directory — use it.
3. If none exists, default to creating `~/Obsidian/` and tell the user in one line what
   you're doing, so they can redirect you if they keep vaults elsewhere.

Record the resolved base directory mentally for the rest of the session — don't re-ask or
re-search on every note, just re-check if the user references a path that doesn't match.

## Step 1 — One vault per project, named to match

Each project gets its own folder directly under the base directory, named with the
project's slug (match how the user refers to the project — e.g. `academy-portal`,
`bi-accelerator`, `sentinel-ai` — lowercase, hyphenated, matching the repo/project name
rather than inventing a new name).

```
~/Obsidian/
├── academy-portal/
├── bi-accelerator/
├── sentinel-ai/
└── <new-project>/
```

**Before creating a new vault, check whether one already exists** for that project
(`ls ~/Obsidian/`, fuzzy-match against existing folder names). If the user is clearly
talking about a project that already has a vault, use that vault — do not create a
second one with a slightly different name (`sentinel_ai` vs `sentinel-ai`).

To initialize a brand-new vault:
```bash
mkdir -p ~/Obsidian/<project-slug>/.obsidian
mkdir -p ~/Obsidian/<project-slug>/{00-Inbox,01-Architecture,02-Decisions,03-Bugs-and-Fixes,04-Reference,05-Meta}
```
The `.obsidian/` folder can stay empty — Obsidian populates its own config the first time
it opens the folder as a vault. Its mere presence is what makes a folder "a vault" rather
than just a directory of markdown files.

Then create the vault's index note immediately (see Step 3) — a vault without an index is
already starting to rot.

## Step 2 — Folder structure and what goes where

Use this structure inside every vault (create only the subfolders actually needed for a
given project — don't pad out empty folders nobody will use):

- **00-Inbox/** — quick captures not yet organized. Fine to leave here temporarily; sweep
  into the right folder when you next touch the vault.
- **01-Architecture/** — how the system is built: modules, data flow, schema notes, stack
  decisions. One note per component/module is better than one giant note.
- **02-Decisions/** — decision records: what was decided, why, what alternatives were
  considered. Use the decision template in `references/note-templates.md`.
- **03-Bugs-and-Fixes/** — postmortems and fix notes worth remembering, especially
  non-obvious root causes. Skip trivial fixes; log the ones with a lesson in them.
- **04-Reference/** — stable facts that don't change often: conventions, API contracts,
  environment setup, glossary of project-specific terms.
- **05-Meta/** — the vault's own index/MOC note, and a running "recent activity" log if the
  user wants one.

Not every project needs all five. A small side project might just get Inbox + Reference.
Match the structure to the project's actual size — read Step 0's memory context (repo
scope, project's known scale) rather than always creating the full skeleton.

## Step 3 — Every vault has one index note (a Map of Content)

`05-Meta/Index.md` (or `<Project-Name>.md` at the vault root, either is fine — pick one
convention and stay consistent within a vault) links out to every other note in the vault,
grouped by the folder structure above. This is the note a person opens first. Use the MOC
template in `references/note-templates.md`. Update it whenever a note is added — an index
that's gone stale is worse than no index, because it actively misleads.

## Step 4 — Note format

Every note gets YAML frontmatter and follows the atomic-note principle — one note per
concept, linked to related notes rather than restating them. Use the templates in
`references/note-templates.md` verbatim (fill in the bracketed fields) rather than
freehanding frontmatter, so notes stay consistent across a vault and across vaults.

Minimum frontmatter on every note:
```yaml
---
title: <note title>
created: <YYYY-MM-DD>
tags: [<project-slug>, <category tag(s)>]
---
```
Link liberally with `[[Note Title]]` wherever a concept has (or should have) its own note.
A note referencing three other concepts should have three `[[wikilinks]]`, not three
inline explanations that duplicate content living elsewhere.

## Step 5 — Creating vs. updating: search before you write

Before writing a new note, search the vault for whether the topic already has one:
```bash
grep -ril "<topic keyword>" ~/Obsidian/<project-slug>/
```
- **Topic has no note yet** → create one in the right folder, add a link to it from the
  index and from any note that references the concept.
- **Topic has a note already** → update that note. Append a dated subsection for new
  information rather than overwriting history, unless the update fully supersedes the old
  content (e.g. a decision that reversed an earlier one — in that case, mark the old
  section `> [!note] Superseded on <date>` rather than deleting it).
- **Never duplicate a concept across two notes** in the same vault. If you find near-
  duplicate notes while working, flag it to the user and offer to merge them rather than
  adding a third.

## Step 6 — What's worth capturing (and what isn't)

Capture: architecture decisions and why, non-obvious bug root causes, conventions the user
has stated (naming, structure, style preferences for that project), anything the user
explicitly says to remember.

Don't capture: routine or trivial changes with no lasting lesson, anything already fully
documented in the codebase (don't duplicate docstrings/READMEs into the vault — link to the
file path instead if it's worth referencing), or session-specific scratch work the user
didn't ask to keep.

## Step 7 — When the user just says "note this down" mid-conversation

Don't interrupt the current task to ask twenty questions. Identify the project from
context, resolve or create its vault per Steps 0–1, write the note into the right folder
per Step 2, link it from the index per Step 3, and confirm in one line what you filed and
where — then get back to what they were doing.
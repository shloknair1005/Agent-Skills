# Note templates

Fill in every `[bracketed]` field. Keep frontmatter keys in this exact order/casing so
notes stay consistent and any Obsidian dataview/query plugin the user adds later can rely
on a stable schema.

Write all prose you put into the fields in simplified technical English (about 80% of the
way to ASD-STE100): short sentences, active voice, simple tenses, plain words, one term
for each concept. See `ste-writing-guide.md` in this folder. Do not change frontmatter,
code, paths, or `[[wikilink]]` titles.

---

## Vault index / MOC (Map of Content)

Path: `05-Meta/Index.md`

```markdown
---
title: [Project Name] — Index
created: [YYYY-MM-DD]
tags: [[project-slug], moc]
---

# [Project Name]

[One short sentence: what this project is.]

## Architecture
- [[Note Title]] — one-line description
- [[Note Title]] — one-line description

## Decisions
- [[Decision: short title]] — one-line description

## Bugs & Fixes
- [[Fix: short title]] — one-line description

## Reference
- [[Note Title]] — one-line description

## Recent activity
Full history with exact changes: [[Activity Log]]
- [YYYY-MM-DD HH:MM:SS +ZZZZ] created [[Note Title]] — short summary
- [YYYY-MM-DD HH:MM:SS +ZZZZ] updated [[Note Title]] — what changed
```

Keep "Recent activity" to the last 10 entries. Put the newest entry at the top and trim older
entries. The Activity Log holds the full history, so nothing is lost when you trim.

---

## Architecture note

Path: `01-Architecture/[Component Name].md`

```markdown
---
title: [Component Name]
created: [YYYY-MM-DD]
tags: [[project-slug], architecture]
---

# [Component Name]

## What it does
[1-3 short sentences. Active voice.]

## How it works
[Key mechanics: data flow, key files and functions, dependencies. One idea in each sentence.
Link to related components with [[wikilinks]]. Do not explain them again here.]

## Related
- [[Other Component]]
- [[Decision: relevant decision]]
```

---

## Decision record

Path: `02-Decisions/Decision - [short title].md`

```markdown
---
title: Decision - [short title]
created: [YYYY-MM-DD]
tags: [[project-slug], decision]
status: [active | superseded]
---

# Decision: [short title]

## Context
[What situation caused this decision. Use simple past tense.]

## Decision
[What we decided. One or two short sentences.]

## Alternatives considered
- [Alternative] — [why we did not choose it]

## Consequences
[What becomes easier. What becomes harder.]

## Related
- [[Component or note this affects]]
```

If a later decision reverses this one, don't delete this note — set `status: superseded`
in the frontmatter and add a line at the top: `> [!note] Superseded by [[Decision: new
title]] on [date]`.

---

## Bug / fix note

Path: `03-Bugs-and-Fixes/Fix - [short title].md`

```markdown
---
title: Fix - [short title]
created: [YYYY-MM-DD]
tags: [[project-slug], bugfix]
---

# Fix: [short title]

## Symptom
[What the user or the system showed. Use simple past tense.]

## Root cause
[The actual cause. Name the thing that failed and the reason. Most important when the cause was not obvious.]

## Fix
[What we changed. Use active voice.]

## Lesson
[What to check next time. What pattern to avoid. Use "must" or "do not" for rules.]

## Related
- [[Component this touched]]
```

Skip this template for trivial fixes (typos, obvious off-by-ones) — only worth a note when
there's a root cause or lesson non-obvious enough to forget by next month.

---

## Reference note

Path: `04-Reference/[Topic].md`

```markdown
---
title: [Topic]
created: [YYYY-MM-DD]
tags: [[project-slug], reference]
---

# [Topic]

[Stable facts: conventions, setup steps, glossary entries, API contracts. Write this as
something that stays true for months, not a snapshot of today's state — if it's about to
change, it's not reference material yet.]

## Related
- [[Note this supports]]
```

---

## Activity Log

Path: `05-Meta/Activity Log.md`

Do not write this note by hand. The script `scripts/vault-log.sh` creates it and adds each
entry (see Step 9 in `SKILL.md`). Never edit or delete an old entry.

`````markdown
---
title: Activity Log
created: [YYYY-MM-DD]
tags: [[project-slug], meta, log]
---

# Activity Log

Full history of changes to this vault. The skill only adds entries at the end.
It never edits or removes an old entry. Times come from the system clock.

## [YYYY-MM-DD HH:MM:SS +ZZZZ] — [action] — `[relative/path.md]`

- **Time:** [YYYY-MM-DD HH:MM:SS +ZZZZ]
- **Action:** [created | updated | superseded | renamed | deleted | external]
- **File:** `[relative/path.md]`
- **Summary:** [One or two short sentences: what changed and why.]
- **Change:** +[n] lines, −[n] lines

<details>
<summary>Exact diff</summary>

````diff
[unified diff]
````

</details>
`````

# Question and pushback guide

Read this before the first discovery round.

**Contents:** 1 Round format · 2 Writing a good question · 3 Pushback · 4 Special answers · 5 Anti-patterns · 6 Example round

## 1. Round format

Use the same shape every round so the user can answer fast:

1. **Understood so far** (2 or 3 lines). Only what is new since the last round.
2. **Pushback** (only if you have one). See section 3.
3. **Questions** (4 or fewer, one topic each).
4. **Coverage** (one line, after the answers).

When you use the `AskUserQuestion` tool, put the options in the tool call and keep the chat text short. When you use plain chat, number the questions and letter the options, and mark the recommended one with "(recommended)".

## 2. Writing a good question

- **One decision per question.** "Who can delete a project, and does delete keep the data?" is two questions. Split it.
- **Concrete options, 2 to 4.** Add "Other" or "Something else". Write options so the user can see the consequence, not just the label: "Soft delete: hidden, can be restored for 30 days" and not "Soft delete".
- **Mark one recommendation** and give a one-line reason. Say what would be reworked if the answer is wrong ("A later change to hard delete needs a data migration").
- **Ground it in the repo.** Cite what you found: "`orders` already has `deleted_at`. Do you want the same pattern for projects?"
- **Ask the product question, not the technical one.** Ask "Must two people edit the same project at once?" and not "Do you want optimistic locking?" Decide the technical answer later from the confirmed product answer, and ask only if two technical options have different user-visible results.
- **Use the user's words** and the terms already in the vault Glossary. One term for each concept.
- **Offer a scenario when the answer is abstract.** "A user uploads a file with 3 bad rows out of 100. Reject all, or import 97 and report 3?"

## 3. Pushback

Push back when you find a materially better path. Do not push back to look critical.

**Triggers**
- An existing feature, component, or library in the repo already does most of this.
- A simpler build gives the same user outcome (for example, a filter instead of a new module).
- The scope is too big for a first release, or the MVP can be cut with no loss of the core outcome.
- A third-party service or standard solution is cheaper than building it.
- The design carries a security, data-loss, or migration risk that the user may not see.
- Two answers or two constraints contradict each other.
- A constraint forces a poor result. Show what relaxing it would give. Only the user can relax it.

**Format**

```
Pushback: <topic>
Your plan: <what the user said>
Alternative: <what you suggest>
Why: <evidence: file path, number, existing feature, or concrete risk>
Cost of the alternative: <what the user gives up>
I recommend: <your plan | the alternative>. Your decision.
```

**Etiquette**
- Make the case once. After the user decides, record it in a `Decision` note (options, trade-offs, who decided, date) and do not raise it again unless there is new evidence.
- If the user chooses their own plan, plan it well. Do not hint that it was the wrong choice later.
- Keep each pushback short. Facts first, no lecture.
- Never change a constraint or a decision because you prefer another one. Ask.

## 4. Special answers

| User says | Do this |
|---|---|
| "I don't know" | Give 2 or 3 options with trade-offs and a recommendation. If it still cannot be decided, record it in `Open Questions` with what is needed to decide (a spike, a person, data). Do not move to Stage 3 while it is open. |
| "You decide" or "defaults" | Record the choice as a `delegated` decision with your reason. List all delegated decisions together at Gate 1 so the user can veto any of them. |
| A vague answer ("make it fast", "simple UI") | Ask for a number or a scenario: "What is too slow: 1 second or 5 seconds, for how many rows?" |
| An answer that contradicts an earlier one | Show both statements with dates and ask which one holds. Mark the older one superseded. |
| A new idea that grows the scope | Add it to the parking lot (C3). Ask whether it is in the first release. If yes, re-check the phase sizes. |
| No answer to a question | Leave it open. Ask it again in the next round. Do not record a default. |
| "Why are you asking this?" | Say what would be reworked if the answer were wrong. If you cannot, drop the question. |

## 5. Anti-patterns

- Asking what the code can answer.
- Asking more than 4 questions in a round, or one long open question.
- Recording a recommended default as a decision before the user picked it.
- Asking technical questions before the product is clear.
- Writing the notes after every message. Write once per round.
- Re-asking a confirmed item. Check `Planning Status.md` first.
- Pushing back on style or naming. The existing repo patterns decide those.

## 6. Example round

> **Understood so far.** Users are team admins and members. Reports are for admins only (A1, B1). Constraint C-03: no new dependencies.
>
> **Pushback: export format.** Your plan: a new PDF export module. Alternative: reuse the CSV export in `services/export.py`, and add a print stylesheet to the existing report page. Why: it covers "admins send a copy to finance" (A1) with no new dependency (C-03). Cost: no custom page layout. I recommend the alternative. Your decision.
>
> **Questions**
> 1. Who can view a report? (a) Admins only (recommended: matches the stated goal) (b) Admins and members (c) Admins, plus members for their own data. *If wrong: a permission change later touches every query.*
> 2. A report covers 50,000 rows. Is a 10 second wait acceptable? (a) Yes, with a progress state (b) No, it must run in the background and send an email (recommended if rows grow). *If wrong: background jobs need a queue we do not have.*
> 3. Treat these as out of scope: report scheduling, report sharing by link, custom columns. Confirm? (a) Confirm (b) One of them matters.

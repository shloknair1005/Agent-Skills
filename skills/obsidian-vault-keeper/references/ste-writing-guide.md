# Writing style: Simplified Technical English (about 80%)

This guide tells you how to write the prose in vault notes and in your explanations to the
user. The model is ASD-STE100 (Simplified Technical English). The target is **about 80% of
the way there**: use the rules below every time, but do not twist a sentence to satisfy a
rule when the result is less clear.

This is a practical subset. It is not the full ASD-STE100 specification and it does not
include the official approved-word dictionary. Do not claim the notes are "STE compliant".

## Contents
1. Where the style applies
2. Core rules (apply every time)
3. Relaxed rules (apply when they cost nothing)
4. What you do not rewrite
5. Before and after examples
6. Self-check before you save

## 1. Where the style applies

Apply it to:
- The body text of every note you write or update in the vault.
- The one-line descriptions in the index note.
- Your explanations to the user about a feature, a system, an enhancement, or a change.
- Your confirmation line after you file a note (Step 7).

Do not apply it to the user's own words when you quote them, or to anything in the "do not
rewrite" list in section 4.

STE is an English standard. If the user writes in another language, write the notes in that
language and keep the same principles: short sentences, plain words, one idea each.

## 2. Core rules (apply every time)

1. **Keep sentences short.** Aim for 20 words or fewer for instructions and 25 or fewer for
   descriptions. Going to 30 is acceptable when a split would break the meaning.
2. **One idea in each sentence.** If a sentence has "and" joining two separate ideas, make
   two sentences.
3. **Keep paragraphs short.** Maximum six sentences. One topic for each paragraph. Start
   with the topic sentence.
4. **Use the active voice.** Name the thing that does the action.
   - Not: "The token is refreshed by the scheduler."
   - Yes: "The scheduler refreshes the token."
5. **Use simple tenses.** Prefer the simple present ("The API returns a list"), the simple
   past ("We chose Postgres"), and the simple future ("The job will retry"). Avoid perfect
   and progressive forms ("has been running", "is going to be") when a simple form works.
6. **Write instructions as commands.** Use the imperative ("Run the migration."). Put one
   action in each step. Use a numbered list when the order matters.
7. **Put warnings before the step they apply to.** Start the line with `Warning:` for a
   risk of data loss or breakage, or `Note:` for other information.
8. **Use plain, common words.** Prefer "use" to "utilize", "start" to "initiate", "show" to
   "display" or "illustrate", "need" to "necessitate", "about" to "approximately".
9. **Keep one word for one meaning.** Pick one term for each concept and use it every time
   in the vault. Do not alternate between "module", "component", and "service" for the same
   thing. Check the Reference notes for the project's chosen term.
10. **Use words for requirement and ability on purpose.** "Must" means a rule. "Can" means
    something is possible. Avoid "should", "may", "might", and "ought to" in rules, because
    their meaning is not firm.
11. **Keep the articles.** Write "the", "a", and "an". Do not drop them to save space.
12. **Break up long noun clusters.** Use at most three nouns in a row. Rewrite longer ones
    with "of", "for", or "in".
    - Not: "user session token refresh failure handler"
    - Yes: "the handler for failed refreshes of the user session token"
13. **No idioms, slang, metaphors, or jokes.** Write "the build fails", not "the build blew
    up". Write "fix", not "nail down". Avoid phrasal verbs with several meanings ("set up",
    "carry out", "figure out") when one plain verb is clearer: "install", "do", "find".
14. **Say what a pronoun refers to.** If "it", "this", or "they" can point to two things,
    use the noun again.

## 3. Relaxed rules (apply when they cost nothing)

These are part of full STE. Follow them when they come naturally. Skip them when they make
the text stiff or unclear. This is the "other 20%".

- Do not stay inside the official approved-word dictionary. Plain common words are enough.
- Do not ban every verb ending in "-ing". Avoid it when it hides who does the action
  ("Using the cache improves speed" is acceptable; "Caching being enabled" is not).
- Do not count words with a stopwatch. A 27-word sentence that reads well is fine.
- Do not remove a technical term that has no simpler form. Keep it and define it once (see
  section 4).
- Do not force a numbered list on a short description. Use it for ordered procedures.

## 4. What you do not rewrite

Keep these exactly as they are:
- Code, commands, file paths, and configuration keys.
- YAML frontmatter keys and values, and the `[[wikilink]]` titles of existing notes.
- Names of products, libraries, APIs, functions, and classes.
- Error messages and log lines (copy them exactly, inside a code block).
- Quotes from the user or from other documents.
- Technical terms with no simpler form. Define each one in one short sentence the first time
  it appears in a vault, and put the definition in a Reference note (`04-Reference/`) if
  the term will come back.

## 5. Before and after examples

**Decision note, Context section**

Before:
> We ended up going back and forth on whether it'd make sense to leverage a queue for the
> email notifications, since the synchronous approach was causing the request handlers to
> get bogged down whenever the SMTP provider was having issues.

After:
> The request handlers sent email directly. When the SMTP provider was slow, the handlers
> were slow too. We considered a queue for the email jobs.

**Bug note, Root cause section**

Before:
> It turned out that the cache key was getting clobbered because the tenant ID wasn't being
> factored in, so data was bleeding across tenants.

After:
> The cache key did not include the tenant ID. Two tenants used the same key. Each tenant
> could read the data of the other tenant.

**Architecture note, How it works section**

Before:
> The ingestion pipeline is kicked off by a cron trigger and then fans out to a bunch of
> workers that each take care of a slice of the data.

After:
> A cron trigger starts the ingestion pipeline. The pipeline sends the data to several
> workers. Each worker processes one slice of the data.

**Reference note, a rule**

Before:
> You should probably avoid putting business logic in the controllers.

After:
> Do not put business logic in the controllers. Put it in the service layer.

**Confirmation line to the user**

Before:
> I've gone ahead and captured that decision in your vault and wired it up to the index.

After:
> I saved "Decision - Use a queue for email" in `sentinel-ai/02-Decisions/` and added it to
> the index.

## 6. Self-check before you save

Read the text once and check these points:
1. Is any sentence longer than about 25 words? Split it.
2. Is any sentence passive without a good reason? Make it active.
3. Does the text have an idiom, a metaphor, or a vague "should"? Replace it.
4. Does one concept have two different names? Choose one name and use it everywhere.
5. Did you change anything from the "do not rewrite" list? Restore it exactly.
6. Is the text still correct and complete? Clarity and accuracy come before style. If a
   rule makes the text less clear, break the rule.

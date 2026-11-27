---
name: enterprise-ui
description: Shlok's default enterprise/internal-tool UI design system — a JPMC/McKinsey-style corporate aesthetic (dark navy sidebar, gold accent, teal actions, Playfair Display serif headers + Inter body, card-based workspace layout). Use this whenever building or restyling the frontend of a Flask app, internal tool, admin dashboard, data/BI/ETL utility, or any project UI for Shlok, even if he doesn't explicitly ask for "enterprise" styling — this is his standard look, not an opt-in extra. Trigger on requests like "build a UI for X", "make a dashboard", "add a frontend/admin panel", "the UI looks basic, make it look professional", or any new project needing HTML/CSS. Do NOT use for public marketing/landing pages, mobile-first consumer apps, or when the user explicitly asks for a different visual style.
---

# Enterprise UI Design System

This is Shlok's default visual language for internal tools, dashboards, and
Flask app frontends — modeled on the look of his BI Accelerator / Academy
Portal projects. Corporate, serious, a little luxurious (JPMC / McKinsey
aesthetic), not a generic Bootstrap admin template.

Apply this by default to any new project frontend unless the user asks for
something else. If a project already has its own established style, don't
overwrite it without asking — but for anything new, greenfield, or
explicitly described as rough/basic/unstyled, use this system.

## Design philosophy (the parts that matter most)

1. **Dark sidebar, light workspace.** The app is always split into a fixed
   dark navigation sidebar (280px) and a light, scrollable content area.
   This contrast is the single most identifying trait of the look — don't
   flatten it into an all-light or all-dark UI.
2. **Serif for identity, sans for interface.** `Playfair Display` is used
   *only* for brand wordmarks, page titles (`h1`), and card headings (`h2`)
   — never for body text, labels, or buttons. `Inter` handles everything
   functional. `Fira Code` is reserved for anything that reads as raw
   system/log output (terminal panel, code-like values). Mixing a serif
   display font with a clean grotesk body font is what makes this feel
   "premium enterprise" rather than "generic dashboard template."
3. **Three-color logic, used consistently, not decoratively:**
   - **Navy** (`--primary-navy`) = identity/headings/admin-weight actions.
   - **Gold** (`--accent-gold`) = the one luxury accent — active nav
     indicator, brand subtitle, outlined secondary buttons in the dark
     sidebar. Used sparingly; if gold shows up everywhere it stops working.
   - **Teal** (`--accent-teal`) = the workhorse action color — primary
     buttons, focus rings, progress bars, most interactive highlights.
   - Success/warning/danger are separate and never borrowed for branding.
4. **Cards, not raw sections.** Every distinct piece of content sits inside
   a `.card` with a `.card-header-bar` (title + optional actions). This
   gives every screen the same rhythm no matter what it contains.
5. **State shown structurally, not just by color.** Status is communicated
   via pills, left-border tints on inputs, and gold left-rails on active
   nav — not by changing text color alone. Look for a "which existing
   pattern communicates this state" answer before inventing a new one.
6. **Fixed-height desktop app shell, not a scrolling webpage.** `body` is
   `height: 100vh; overflow: hidden;` — only `.content-scrollable` scrolls.
   This is intentional: it's an internal tool, not a marketing site. Don't
   add responsive breakpoints or page-level scroll unless explicitly asked.
7. **Utilitarian over flashy.** Native `alert()`/`confirm()` for simple
   confirmations, inline `.action-container` swaps instead of modal
   overlays, plain animations (`ease` transitions, a breathing status dot,
   a spinner) — nothing gratuitous. The "premium" feeling comes from
   typography and color discipline, not from motion or ornamentation.

## Workflow: applying this to a new or existing project

1. **Copy the base stylesheet.** Copy `assets/base.css` into the project
   (e.g. `static/css/base.css` for a Flask app) unmodified except for the
   `:root` variable values if the project needs its own brand color
   instead of the navy/gold/teal defaults. Never rename the CSS variables
   or restructure selectors — other snippets in this skill and in past
   projects depend on those exact names.
2. **Set up the shell.** Use `assets/template.html` as the starting
   skeleton: `<link>` the three Google Fonts, then `.app-shell` >
   `.sidebar` + `main.workspace` (`.topbar` + `.content-scrollable`).
   Replace `{{ BRAND_NAME }}` / `{{ PRODUCT_NAME }}` / `{{ PROJECT_TAGLINE }}`
   with the project's own name — ask the user for these if not obvious
   from context, don't invent a fake brand name.
3. **Build content as cards inside `.content-scrollable`.** Pull specific
   component markup from `references/components.md` (buttons, cards,
   forms, tables, pills, KPI tiles, accordions, terminal/log panel, loading
   states) rather than writing new CSS from scratch — the point of this
   skill is visual consistency across projects, so reuse > reinvent.
4. **Wire up tab switching** the way `template.html` does: one
   `section#view-<id>` per sidebar tab, toggled via a small `switchTab()`
   function. For multi-step workflows, hide later tabs with
   `style="display:none;"` until earlier steps unlock them (see BI
   Accelerator: mapping tab is available immediately, ETL/Aging tabs
   appear only after a client + use case is loaded).
5. **Only introduce a new component pattern if nothing in
   `references/components.md` fits** — and if you do, follow the existing
   conventions (CSS variables, `--transition-smooth`, the navy/gold/teal
   logic in item 3 above) so it reads as part of the same system, then
   consider whether it's generic enough to add to that reference file for
   future projects.

## When NOT to use this system

- Public-facing marketing pages, landing pages, or anything that needs to
  work well on mobile — this shell has no responsive behavior by design.
- A project where the user explicitly requests a different look (e.g.
  "make it playful," "match this Figma," "light and minimal SaaS style").
- Don't force this aesthetic onto a project that's already consistently
  styled another way — ask before restyling existing, working UI.

## Reference files

- `references/components.md` — copy-paste markup + notes for every
  component (buttons, cards, forms, tables, pills, KPI tiles, accordions,
  terminal panel, loading states, sidebar nav conventions), plus a list of
  things this system deliberately omits (modals, responsive breakpoints).
- `assets/base.css` — the full design-system stylesheet, ready to drop
  into a new project.
- `assets/template.html` — a minimal working shell (sidebar + topbar +
  one tab + one card) to start a new screen from.
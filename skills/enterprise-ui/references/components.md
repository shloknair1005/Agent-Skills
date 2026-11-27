# Component Patterns

Copy-paste snippets for each component. All rely on the CSS variables and
classes defined in `assets/base.css` — don't redefine colors inline, always
use the variables (`var(--accent-teal)`, etc.) so re-theming stays a one-file change.

## Buttons

```html
<button class="btn" onclick="save()">Save to Database</button>
<button class="btn btn-outline" onclick="cancel()">Cancel</button>
<button class="btn btn-outline-danger" onclick="remove()">Delete</button>
<button class="btn btn-admin" onclick="openAdmin()">Admin Action</button>
<button class="btn btn-sm">Compact</button>
<button class="btn" disabled>Disabled</button>
```

Rules:
- Default `.btn` (teal) is the primary/affirmative action on a card — there
  should usually be only one true primary action visible at a time.
- `.btn-outline` is secondary/neutral (cancel, view, export).
- `.btn-outline-danger` for destructive actions — never make delete the
  filled/primary color.
- `.btn-admin` (navy) marks an action as privileged/developer-only, visually
  distinct from ordinary workflow actions.
- A one-off custom accent (e.g. `style="background:#5B21B6;"`) is acceptable
  for a clearly distinct action class (like "download a different bundle
  type") but shouldn't become the default — reach for the four button
  classes above first.

## Cards

```html
<div class="card">
    <div class="card-header-bar">
        <div>
            <h2>Section Title</h2>
            <p class="sub-desc">One-line description of what this card does.</p>
        </div>
        <button class="btn">Action</button>
    </div>
    <!-- card body -->
</div>
```

- Every card is a `.card`. Cards stack vertically in `.content-scrollable`
  with `margin-bottom: 2rem` (already baked into `.card`).
- `.card-header-bar` always goes at the top: title (serif `h2`) + optional
  sub-description on the left, actions on the right.
- Use `.admin-card` (colored top border) to visually flag a card as an
  administrative / configuration panel, distinct from regular workflow cards.

## Forms

```html
<div class="form-grid-2">
    <div class="form-group">
        <label>Client Name</label>
        <input type="text" class="form-control" placeholder="Acme Corp">
    </div>
    <div class="form-group">
        <label>Use Case</label>
        <select class="form-control"><option>Sales</option></select>
    </div>
</div>
```

- `.form-grid-2` / `.form-grid-3` for side-by-side fields; stack with plain
  `.form-group` blocks for a single column.
- Labels are always small, bold, slate — never rely on placeholder text
  alone as a label.
- Focus state (teal ring) is automatic via `.form-control:focus` — don't
  override it per-field.

## Tables

```html
<div class="table-responsive">
    <table>
        <thead>
            <tr><th>Column</th><th style="text-align:center;">Status</th></tr>
        </thead>
        <tbody>
            <tr>
                <td>Value</td>
                <td style="text-align:center;"><span class="pill pill-mapped">Mapped</span></td>
            </tr>
        </tbody>
    </table>
</div>
```

- Always wrap `<table>` in `.table-responsive` for the border/radius/scroll.
- Header cells are uppercase, small, muted — never bold-and-dark; that's
  reserved for cell content the user should focus on.
- Use inline `style="width: X%;"` on `<th>` to control column proportions
  for wide data tables — this codebase favors explicit column widths over
  letting the browser auto-size.
- Status inside a table cell → use a `.pill`, not colored text.

## Status pills / badges

```html
<span class="pill pill-mapped">Mapped</span>
<span class="pill pill-unmapped">Unmapped</span>
```

Define new `.pill-*` variants the same way: light background tint + dark
text of the same hue, uppercase, rounded-full. Reuse `--success` /
`--warning` / `--danger` tints where the badge maps directly to one of
those states.

## Left-border status inputs

For a `<select>` or `<input>` whose state (mapped/valid vs.
unmapped/needs-attention) matters at a glance in a dense table, tint the
left border instead of adding an icon column:

```html
<select class="form-control select-source mapped">...</select>
<select class="form-control select-source unmapped">...</select>
```

## KPI tiles

```html
<div class="kpi-grid">
    <div class="kpi-tile">
        <div class="kpi-val">1,204</div>
        <div class="kpi-lbl">Records Processed</div>
    </div>
</div>
```

Use for summary metrics at the top of a workspace view. `.kpi-grid` is
auto-fit responsive (`minmax(180px, 1fr)`) — just keep adding `.kpi-tile`
children, don't hardcode a column count.

## Accordions

```html
<button class="accordion" onclick="toggleAccordion(this)">
    Section Label
    <span>▾</span>
</button>
<div class="panel">
    <!-- expandable content -->
</div>
```

```js
function toggleAccordion(btn) {
    btn.classList.toggle('active');
    const panel = btn.nextElementSibling;
    panel.style.display = panel.style.display === 'block' ? 'none' : 'block';
}
```

Active accordions use the violet tint (`#EDE9FE` / `#5B21B6`) — this is the
one deliberate departure from navy/teal/gold, reserved specifically for
"currently expanded" state so it's unambiguous against pills and buttons.

## Terminal / log console

```html
<div class="terminal" id="pipelineTerminal">
    <div class="term-line"><span class="term-time">[System]</span> Awaiting job trigger...</div>
</div>
```

```js
function logLine(terminalEl, message) {
    const line = document.createElement('div');
    line.className = 'term-line';
    line.innerHTML = `<span class="term-time">[${new Date().toLocaleTimeString()}]</span> ${message}`;
    terminalEl.appendChild(line);
    terminalEl.scrollTop = terminalEl.scrollHeight;
}
```

Use this whenever a project needs to show pipeline/job/ETL output — it
reads as "engineering telemetry," which fits the enterprise-tool feel far
better than a plain `<pre>` block or a spinner-only state.

## Loading / empty / success state block

```html
<div class="action-container" id="loadingState" style="display:flex;">
    <div class="spinner"></div>
    <h3>Refining schema mapping...</h3>
    <p style="color: var(--text-muted); font-size: 0.9rem; margin-top: 0.5rem;">
        This may take a few seconds.
    </p>
</div>
```

Toggle `display: none` / `flex` on `.action-container` rather than building
a separate modal/overlay system — in this design language, transient states
replace the card content area inline instead of floating over it.

## Sidebar navigation

- Sidebar is always dark (`--bg-sidebar`) regardless of how light the rest
  of the app is — this contrast is central to the aesthetic, don't lighten it.
  Brand wordmark is serif (Playfair) with an uppercase Inter subtitle
  underneath (product name, e.g. "BI Accelerator").
- Nav buttons (`.tab-btn`) get a 3px gold left-rail when `.active`, not a
  background-only highlight — always pair the gold accent with the active tab.
- Progressive disclosure: hide tabs the user hasn't unlocked yet with
  `style="display:none;"` and reveal them via JS as prerequisite steps
  complete, rather than showing every tab from page load.
- Footer of the sidebar is for secondary, less-frequent actions (admin
  toggles, external monitoring links) — outlined gold buttons, not filled.

## Alerts / confirmations

This design language uses native `alert()` / `confirm()` for simple
confirmations and error messages rather than custom toast/snackbar
components — it's a deliberate "utilitarian internal tool" choice, not an
oversight. Keep using native dialogs for quick confirmations unless a
project specifically asks for richer, non-blocking notifications; if it
does, build a small `.pill`-styled toast rather than introducing an
unrelated visual language.

## What this system deliberately does NOT have

- No mobile breakpoints / responsive layout — `body` is `height: 100vh;
  overflow: hidden;`, designed for a fixed desktop workspace. Don't add
  `@media` queries unless the project explicitly needs a responsive/public
  page (in which case treat that page as outside this design system, e.g.
  a marketing landing page, and keep the app shell above for the actual tool).
- No modal/dialog component — inline `.action-container` swaps and
  `.card`-level state changes are used instead. Introduce a real modal only
  if a project genuinely needs to block interaction with the rest of the
  screen (e.g. a destructive confirm with details) and reuse `.card` styling
  for its content.
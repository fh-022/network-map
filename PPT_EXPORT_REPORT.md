# Platform UX Review — Status Quo Critique
2026-07-13 · based on a full walkthrough of the current build (2,359 dealers, 4 markets)

## Summary verdict

The platform is analytically strong but organized like an engineer's control panel, not like a consultant's workflow. Every feature works; the problems are placement, prominence, guidance, and consistency. A user who wasn't in the room when we built it needs ~15 minutes of confusion before productivity. The good news: most fixes are re-arrangement and micro-copy, not rebuilds.

---

## 1. Information architecture — the biggest issue

**Findings**
- Features are scattered across five containers with no workflow logic: left panel (3 tabs), 4 top-bar buttons, one modal launched from *inside the Filter tab* (coverage build-up), plus dialogs.
- The **Analysis block (drive time + KPI) lives at the bottom of the Filter tab** — the single most important output of the tool is below two giant filter lists and appears/disappears depending on tab.
- **Exports live in three unrelated places**: PPT in the top bar, location CSV inside Filter, thinkcell Excel inside the build-up modal, directory CSV inside the drawer. A user who wants "give me my outputs" has to know all four spots.
- The coverage build-up — analytically one of the strongest features — is hidden behind a small text button at the bottom of a scrolled-out filter panel. Nobody will find it.

**Suggestions**
- Restructure the left panel around the consulting workflow, not data types: **① Scope (market/filters, collapsed by default) → ② Plan (case, scenario, places) → ③ Results (KPI, coverage curve, comparisons)**. The KPI belongs permanently visible at top or bottom of the panel, in every tab.
- One **"Exports" home** (top-bar button) listing all four export types with one-line descriptions. The existing dialogs can stay; this is just a router.
- Promote coverage build-up to a first-class tab or a Results-section card with a mini-preview sparkline of the active case's curve — the sparkline itself is the button.

## 2. First-run experience & guidance

**Findings**
- Cold start shows: a wall of filters, KPI reading "– / no sites in measure", and no hint what to do. The core loop (pick markets → add places by clicking map → tune drive time → read coverage → export slide) is nowhere narrated.
- "Case", "Scenario", "Workspace", "Measure", "Compare" are all unexplained jargon in tiny labels. Three nesting levels (workspace > case > scenario) is a lot to hold.

**Suggestions**
- Empty-state coaching: when the active scenario has zero places, replace the KPI block with a 3-step mini-guide ("1. Choose markets · 2. Click the map to place a site · 3. Read coverage here") with the map hint pulsing once.
- Rename toward consulting language: **Case → "Market case"** stays, **Scenario → "Network variant"**, and show the hierarchy as a breadcrumb in the top bar: `All markets ▸ Variant: Base`. One glance = full context.
- The ⚠ est. chip should open a one-paragraph plain-language explanation (the ±20–30% disclaimer we already wrote) on click — currently it's a mystery glyph.

## 3. Filter tab — right features, wrong weighting

**Findings**
- Brand and Group multi-select lists visually dominate (~60% of panel height) although they're occasional-use power filters. Market, dealer type, CN — the filters consultants touch constantly — are compressed at top.
- The Group list mixes market headers and groups in one scroll; with 80+ groups it's now unwieldy.
- Everything is expanded always; there's no notion of "active filters" summary. After filtering, the only trace is the counter — you can't see *which* filters bite without scrolling the whole panel.

**Suggestions**
- Collapse Brand and Group into accordions, closed by default, with a badge showing active selections ("Brand: 3 selected").
- Add an **active-filter chip row** under the counter ("AT ✕ · Groups only ✕ · MG ✕") — one click removes; "Reset all" appears when anything is active. This is the single highest-value filter UX fix.
- Group list: group by market with collapsible headers, and show location counts per group ("Denzel Gruppe · 19").

## 4. Plan tab — the core, underserved

**Findings**
- Adding places by map click is fine once known, but assignment of existing dealers, priorities (A/B/C), and the "measure" select interact in ways only we understand. "Measure: planned network" vs existing vs both changes the KPI silently — a wrong reading here goes straight into a client slide.
- Compare (vs another scenario) renders one extra KPI row — easy to miss that comparison mode is even on.
- Place list rows are dense; renaming and reprioritizing require precise small-target clicks.

**Suggestions**
- Make the measure choice **visually explicit in the KPI itself**: e.g. KPI header "Coverage — planned sites only" in the accent color, so a screenshot always self-documents what it shows. (This also protects the slides.)
- When Compare is active, render a delta chip next to the KPI ("+6.2pp vs Base") instead of a table row — that's the number consultants actually want.
- Larger touch targets on place rows; drag-to-reorder for priority feels natural and removes the A/B/C dropdown fiddling.

## 5. Directory — good data, heavy delivery

**Findings**
- One table renders all 2,359 rows at once — scroll performance degrades and the browser jank is noticeable; comments truncate with no way to read full text; no indication that clicking a row does anything (does it?).
- Edit (✎) works but there's no visual diff of what has been overridden vs. source data — dbEdits are invisible until you stumble on them.
- The Groups tab and the group filter in the map panel don't cross-link: finding a group in the directory doesn't offer "show on map".

**Suggestions**
- Virtualize or paginate at ~100 rows; add a full-text tooltip or expandable row for truncated cells.
- Mark edited cells with a subtle corner triangle + "edited" filter toggle, and an "undo to source" per cell — trust in the data requires seeing what's been touched.
- Row action "📍 Show on map" (zoom + highlight + set filters to that group). This turns the directory from a viewer into a navigation instrument.

## 6. Export dialog — powerful, but blind

**Findings**
- ~14 toggles, frame chips, label controls, preset list — with zero preview. Users configure blind, generate a whole PPT, open it, discover the legend overlapped a cluster, repeat. Iteration loop is minutes long.
- Preset semantics (live-save, "applies immediately, no Save needed") are explained only in a hover tooltip; the relationship "preset ↔ current map view" stays murky.
- Naming: "Areas: off/union/per-place" — internal vocabulary.

**Suggestions**
- A small static **preview thumbnail** (canvas snapshot of current map + mock title bar) inside the dialog, updating on toggle changes. Even a rough one kills the blind-iteration loop.
- Split the dialog visually: "What's on the slide" (content toggles) / "Which region" (frame) / "Slide text" (title). Same controls, grouped by the question the user is answering.
- Plain-language relabeling and a "copy settings from current view" affordance on presets.

## 7. Coverage build-up modal

**Findings**
- The band drag-handles are invisible until discovered by accident; nothing says "drag me". The +x% gain labels are tiny. Mode switch (scenario coverage vs population fragmentation) changes the entire meaning of the chart with no explanatory sentence.
- The thinkcell export buttons sit here and only here.

**Suggestions**
- Visible drag handles (vertical grip lines with cursor change + one-time tooltip "drag to set bands").
- One caption line under the chart that always states, in words, what is displayed: "Cumulative % of AT demand covered as sites are added, best-first (Case: All markets, 30 min)". This sentence is also exactly what a partner asks in review.
- Keep the exports here but mirror them in the central Exports home (see §1).

## 8. Consistency & polish (cross-cutting)

- **Mixed language**: UI English, data German/Czech, some labels ("Verkauf + Service") leak through — fine for you, but decide one UI language and translate leaked strings in display (keep source data untouched).
- **AT with 0 verified brand split**: VW-Group AT dealers show brand "VW Group" — the map brand filter now contains a pseudo-brand. Either style it distinctly ("VW Group (unspecified)") or exclude it from the brand filter list to avoid confusion.
- **Legend** is static bottom-right; when color-by changes to Ownership the legend must visibly re-title itself (verify).
- **Settings** button contents vs Layers tab overlap (basemap, dim, glass) — merge into one place.
- **Undo**: destructive actions (delete scenario, delete custom place) have no undo; a 5-second "Undone?" toast would cost little.

---

## Priorities

**Quick wins (hours, high impact)**
1. Active-filter chip row + reset (§3)
2. KPI self-documenting header incl. measure + weighted state (§4)
3. Coverage build-up: visible drag handles + caption sentence (§7)
4. Empty-state 3-step guide (§2)
5. Brand/Group accordions collapsed by default (§3)

**Medium (a focused session each)**
6. Exports home / router (§1)
7. Directory: show-on-map row action + edited-cell marking (§5)
8. Export preview thumbnail (§6)
9. Directory virtualization (§5)

**Structural (worth a dedicated iteration)**
10. Left-panel re-architecture into Scope / Plan / Results (§1)
11. Naming pass + breadcrumb context (§2)

My recommendation: do 1–5 as one "usability pass" now, then 6–9, and only then decide whether 10 is still needed — the quick wins may relieve most of the pressure.

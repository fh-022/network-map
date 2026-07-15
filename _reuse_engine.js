# Feature — Market Fragmentation (Population)

## Where it lives
Analysis card → **📊 Market fragmentation (by population)** opens a dedicated panel (as discussed, the corner card was already tight). Shows a cumulative-reach curve: municipalities ranked by raw population, largest first, x-axis = municipality rank, y-axis = % of the case's total addressable population covered as you add them.

## As specified
- **Municipality-level** (census units already in the tool), not split into districts — matches your "Vienna is fine" answer.
- **Raw population**, not the weighted/motorization-adjusted figure used elsewhere in the tool.
- **Respects the active case's markets** — switch case, the curve updates (verified: CZ+SK+CH → 30 rows headed by Prague, vs. a CH-only case → 30 rows headed by Zürich at 9.8%).
- **Top-N as a select**, not a slider (10/20/30/40/50/All), plus the automatic 3-band grouping with average incremental-%-per-city, same idea as your reference slide.
- Full sortable table beneath the chart (rank, municipality, market, population, cumulative population, cumulative %, incremental %).

## Exports
- **CSV**: rank, municipality, market, population, cumulative population, cumulative %, incremental % — ready for thinkcell's data table.
- **PPT slide**: a native, fully editable slide built to match your reference slide's structure — band rectangles with "ø ~X% increase per city" captions, gridlines, the cumulative curve, points, the Top 10/25/All summary table, and the two insight callouts, all as real PowerPoint shapes.
  - **The label boxes are the point of this**, per your note: since thinkcell can't auto-place data labels, the export drops one small textbox per point ("Zürich +9.8%" etc.), pre-positioned right next to its point, ready for you to nudge into a clean, non-overlapping layout by hand instead of typing them from scratch. Dense sets (>22 points) auto-thin the labels (first 12 + evenly spaced + last) to avoid a wall of text; every point still gets its dot even if unlabeled.

## Verified
Chart renders correctly for both a 3-market case (30 rows, Prague-led) and a single-market case (Zürich-led, 9.8% for the top city alone); switching top-N updates chart, table, and CSV consistently; PPT export produces a 112-shape slide — 44 band/table rects, 37 curve/gridline segments, 30 data points, 22 label boxes, one native summary table — with zero JS errors.

## Note on scope
This is the **market-structure view** (independent of any dealer network) that you specified. The complementary "how many places do we need to reach 80% coverage" view — same shape of chart, but x-axis = places in the plan and y-axis = drive-time coverage from the existing engine — is a natural extension using the same panel and export, and I designed the code so it's a straightforward add later if useful.

---
# Update — Excel Export, Dialog UX, Label Overlap

**Excel export (replaces CSV).** Matches your thinkcell data-sheet layout: row 1 "Category" with the rank numbers, "100%=" and "Series" caption rows, then the data row "Addressable market (TAM 1)" with cumulative population values — verified cell-by-cell against a rebuilt version of your screenshot. A second sheet ("detail") carries the full table (population, cumulative %, incremental %) for your own reference; only the first sheet is meant for pasting into thinkcell. One honest limitation: the free Excel-writing library this offline tool uses can't reproduce the peach header coloring from your screenshot — only real spreadsheet software (or thinkcell itself) applies that. The structure and values are exact; the color is cosmetic and thinkcell won't need it to parse the paste.

**Dialog UX.** Every dialog now closes by clicking outside it (the backdrop) or via a small ✕ in the top-right corner, alongside Esc as before. Verified this doesn't break the comment/prompt editor's cancel logic, which needed care since it resolves a promise rather than just closing a box.

**PPT label overlap.** Labels for the fragmentation chart now alternate above/below their point instead of all sitting above, cutting overlap roughly in half for dense charts. Verified positions alternate correctly point-by-point. You'll still want to nudge the densest early cluster apart by hand (same as the reference slide's zoomed-in top-10 callout), but there's markedly less to untangle now.

---
# Update — Scenario Coverage Build-Up (new primary mode)

The panel (Analysis card → "📈 Coverage build-up & market structure") now has two integrated modes via chips at the top:

**Scenario coverage (new, default).** X-axis = your scenario's places, **ordered by marginal gain** (greedy: each next point is the place adding the most coverage on top of those before it). Y-axis = cumulative % of demand within the current drive-time threshold, following the Analysis card's threshold and weighting — and computed with the exact same semantics as the KPI, so **the curve's endpoint always equals the KPI to the decimal** (verified: 81.96% = 81.96%). Single-scenario view shows per-point labels ("Praha +28.5pp") and the ø-per-place bands; the table lists sequence, assigned dealer, marginal gain, and cumulative %, which doubles as a rollout order.

**Comparison across scenarios and cases.** Chips list every scenario in every case (with place counts); tick any combination for overlaid curves in distinct colors with end labels. Each curve honestly uses **its own case's markets** as the 100% base — a CZ-only scenario and an all-markets scenario are each measured against their own addressable demand, stated in the legend.

**Population fragmentation** stays as the second mode, unchanged, with its top-N control appearing only there.

**Exports adapt to the mode.** Excel (thinkcell layout): in coverage mode, Category = place names in greedy order, "100%=" carries the absolute demand base, data row = cumulative covered population; multiple selected scenarios come as stacked blocks; detail sheet includes marginal gains. PPT: single scenario = the full reference-slide treatment (bands, alternating draggable labels, 5/10/all summary table); comparison = colored curves with end labels and a per-scenario summary table.

Verified end-to-end with a rebuilt version of your 12-place CZ scenario at 40 min: greedy order starts Praha +28.5pp; curve ends exactly at the KPI; cross-case comparison (CZ 12 places → 82% vs. all-markets 3 places → 31%) renders and exports correctly; population mode regression-tested intact.

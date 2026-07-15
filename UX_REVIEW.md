# Data Update — Merged Dealer Base (v3 merged)

## New data basis
- **1,362 locations** (was 440): 461 dealer-group sites + **901 independent dealers** — all geocoded (78 district-precision in metros, 1,284 city/village-precision, 0 missing, 0 outside country bounds). The gazetteer grew to ~1,030 places to cover the many new villages; village-center precision, disclaimed as before.
- **65 groups** (was 42) with the new columns: Sales volume estimates now shown in the Directory; the removed "Expansion readiness" column is retired throughout.
- Independent dealers carry ownership type "Independent" and get automatic Chinese-brand detection from their brand list (BYD, MG, Omoda/Jaecoo, Leapmotor, GWM, Xpeng, etc.).

## Dealer-type filter
New filter "Dealer type": **Dealer groups / Independent** chips, right at the top of the Filter tab. Works everywhere downstream — density layers, coverage %, candidate pools, exports. Ownership filter and color-by gained an "Independent" class (green). The group filter list shows the 65 groups by market; the 901 independents appear via search (type 2+ letters) to keep the list usable.

## Comments, integrated
Your two columns are now first-class citizens:
- **Directory → Groups**: "Access ✎" and "Comment ✎" are editable inline. Source values from the Excel prefill them; your edits are stored as **workspace overrides** (exported/imported with the workspace, the Excel is never touched; overridden cells show a tooltip).
- **Planner**: every candidate card shows the access assessment and the 💬 comment, with a 💬 button to add/edit right there. Independent dealers can be commented the same way.
- **Popups**: comment shown, plus an add/edit button.
- **Directory → Locations**: comment column + 💬 action per row; new Type column.
- CSV exports include Access and Comment (effective values incl. overrides).

## Comments now steer the ranking
Candidate scoring replaces the retired readiness field with your access assessment, weighted heavily (50% drive time, 30% access, 20% priority): "Ja" / "Ja, M.D." ≈ 1.0 · "Machbar" ≈ 0.65 · empty ≈ 0.45 · **"Nein" / "Nicht sinnvoll" ≈ 0.05**. Verified effect: for a Praha place, Louda ("Ja (BYD)") and Porsche Inter Auto ("Ja, M.D.") lead, while AURES ("Nicht sinnvoll") drops out of the top despite being closest.

## Verification (headless, zero JS errors)
1,362 markers load (~4 s init, file now 0.68 MB); type filter splits exactly 461/901; coverage of all existing dealers ≤30 min: **95%** (up from 91% — independents fill rural gaps; calc 225 ms); Directory shows 65 groups with source comments; comment override edited, shown on candidate cards, and persisted across reload.

---

## Austria extension (2026-07-13)

**Scope**: Austria added as 4th market (violet #6b4fa0). Existing workspaces untouched; new "All markets" cases include AT. AT dealer count is currently 0 — fills automatically as Perplexity batches (P8-P12) are merged and the platform is rebuilt.

**Demand base**: 275 municipalities ≥5,000 inhabitants, covering 5.69M of 9.16M residents (62.1%) → national scale factor 1.611 (same methodology as CZ 60.5% / SK 51.8% / CH 47.5%). Vienna is a single demand point, consistent with Praha.

**Sources & epistemics**:
- Wien 2,005,760 and Feldkirch 36,384: verified, ZMR 1.1.2024 (Wikipedia, Statistik Austria register data). citypopulation.de and the Statistik Austria ODS were not machine-readable in this environment.
- All other municipal populations: knowledge-based estimates ~1.1.2024, ±10%. Demand shares are dominated by the verified/well-known top layer; tail municipalities (5-8k) carry <0.1% weight each.
- Motorization weights (weighted demand mode): official Statistik Austria Kfz-Bestand 31.12.2024 (press release 2025-02-25), Pkw per 1,000 inhabitants normalized to national avg 569: Burgenland 1.22, Niederösterreich 1.16, Kärnten 1.16, Oberösterreich 1.13, Steiermark 1.10, Salzburg 1.01, Tirol 0.97, Vorarlberg 0.95, **Wien 0.64**. Note: weighted mode visibly down-weights Vienna — analytically correct (363 vs 569 Pkw/1000).

**Road network**: 330 synthetic edges along real corridors (A1, A2, A4/A6, A5, A9, A10, A12, A14, S6, S10, S16 Arlberg, main valley roads), same speed classes and ±20-30% accuracy as other markets. Cross-border edges only between covered markets: Wien–Bratislava (A6/A4, ~42 min), Weinviertel–Mikulov/Znojmo/Brno, Mühlviertel–České Budějovice/Český Krumlov, Rheintal–St. Gallen/Altstätten/Buchs. **No German transit**: Salzburg–Tirol routes internally (Zell am See corridor), so Wien–Innsbruck shows ~6h instead of the real-world ~4h45 via Deutsches Eck; Bregenz–St. Gallen included via St. Margrethen.

**Vienna geocoding**: 23 district PLZ (1010-1230) resolve to Bezirk centroids, analogous to the Praha PSČ rule.

**Verification (headless)**: 1,913/1,917 dealers geocoded (4 rows lack any city info); Wien–Bratislava 42 min, Wien–Graz 124 min, Feldkirch–St. Gallen 48 min; Wien place @45 min covers 47% of AT weighted demand; pre-existing workspaces load unchanged with identical coverage values; zero JS errors.

### Austria dealer data — first fill (2026-07-13, source-first v2 research)
367 AT dealer locations ingested from three verified static sources: Porsche Bank Händlerverzeichnis PDF (258 entries, full enumeration — VW Group dealers; per-brand ticks not decodable, tagged as "VW Group"), group Standorte pages (PIA 43 w/ explicit brands, Denzel 19 merged multi-brand, Pappas 21, Merbag 6, Eisner, AutoFrey), and the Mazda Händlerverband member PDF (47 entries — dated 2019, flagged). Cross-source dedupe by street: 410 raw rows → 367 unique locations. All geocoded (102 rural villages added to gazetteer). The earlier locator-based AT session was discarded after fabricated entries were detected (PIA locations listed as Toyota dealers); details and remaining AT gaps in the workbook's Research Status sheet.

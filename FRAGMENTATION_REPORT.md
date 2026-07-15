# Update — Workspace Completeness & Custom Entries

## Persistence audit result
Already covered: cases (scenarios, places, assignments, alternatives, locks), all Directory edits and overrides (priority, notes, access, comments), excluded locations, PPT presets incl. frames, basemap/dim/glass, threshold and measure.

**Gaps found and closed** — now also stored (and therefore in every workspace export):
- All layer settings: densities incl. their sliders, coverage gaps, hover isochrones, radius circles, city labels, road network, and the demand-weighting toggle.
- Marker color-by.
- **All planner settings, per case:** proposal (objective, N, target %, spacing, min demand, source, live toggle) and assignment constraints (CN, priority, must/must-not sell, max per group). Switching cases restores each case's own settings.
- Robustness: the workspace now also saves synchronously when the tab closes or goes to background, so a change made one second before closing the file can no longer be lost to the auto-save delay (verified with a worst-case instant reload).

**Deliberately session-only** (stated, not forgotten): the map filters (search, market chips, brands, groups, dealer type), the compare selection, and which panel tab is open. Rationale: these are momentary lenses, and reopening the tool with a stale invisible filter ("where are my dealers?") causes more confusion than re-clicking costs. Say the word if you disagree, the mechanism now exists to persist them too.

## Custom groups & locations
Directory → **+ Add** (button adapts to the active tab):
- **Location:** name, group (pick an existing one from the list, type a new name, or leave empty for an independent under its own name), market, type, address, brands, and position via **📍 Pick on map** (click the map; the name auto-suggests the nearest town) or manual Lat/Lon.
- **Group:** name, market, ownership, brand portfolio, Chinese-brand flag, access, comment.
- Custom entries are full citizens: they appear in filters, on the map, as optimizer/assignment candidates (a custom location with access "Ja" ranked 88% and first in testing), in exports, and in the PPT. Chinese-brand detection runs automatically from the brand list for independents.
- Marked with a "custom" badge in the Directory; 🗑 deletes them with full reference cleanup (locks, place assignments, alternatives, exclusions — verified: an assigned+locked custom location was deleted and the place correctly reverted to open).
- Stored in the workspace: export/import carries them; the Excel is never touched. A future prep-run of a new Excel does not overwrite them.

## Open items (dev status)
- **Phase 5b (the formally planned closing round)** is still open: full regression across all features, wording/disclaimer polish, and your collected small-change list from earlier testing — this is the natural next step.
- Editing a custom entry = delete + re-add (no edit dialog yet).
- Export preset list: order = slide order, no drag-reorder.
- Map filters not persisted (by design, see above).
- Known cosmetic: density/frame captures briefly flash on the map during export.
- Ideas parked, say if wanted: writing your Directory edits back into an Excel copy (round-trip), place-table slide in the PPT export, PDF export.

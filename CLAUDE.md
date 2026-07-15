# Perplexity Deep Research — Prompt Pack AUSTRIA (P8–P12)

**Context:** Austria is a new market for the database — there is no existing baseline. Every prompt therefore includes the "Operated by dealer group" column (this matters most), and the VW Group gets its own full prompt since no group research pre-covers it here.

**How to use:** Run each prompt as a separate Deep Research query. Paste results back raw — same ingestion pipeline as CZ/SK/CH.

**Priority order if time is short:** P9 → P10 → P8 → P11 → P12.

---

## PROMPT P8 — Austria: VW Group (full sweep)

You are compiling an exact, dealer-level register of authorized NEW-CAR SALES dealerships in AUSTRIA. Work ONLY from official brand dealer locators and official importer websites (Porsche Holding Salzburg / Porsche Austria GmbH & Co OG is the importer for all VW Group brands — porscheaustria.at, vw.at, skoda.at, audi.at, seat.at, cupraofficial.at). Enumerate every entry.

Brands in scope: **Škoda, Volkswagen (Pkw), VW Nutzfahrzeuge, Audi, SEAT, CUPRA, Porsche**.

For EACH brand output:
1. One line: `TOTAL <Brand> AT: <n> sales outlets, <m> service-only outlets (source URL, accessed <date>)`
2. One markdown table with EVERY outlet:

| Dealer name | Legal company | Street | Postal code + City | Bundesland | New-car sales (Y/N) | Service (Y/N) | Operated by dealer group (name if known) | Source URL |

Rules: preserve German umlauts exactly; distinguish "Betrieb/Händler" (sales) vs "Servicepartner" (service-only) precisely; where an outlet belongs to a known dealer group (e.g., Porsche Inter Auto/PIA, AVAG, Denzel, Pappas, Eisner, Vogl+Co, AutoFrey, Keusch), name the group — this is a core deliverable. Do NOT invent entries; "enumerated X of Y" is a good answer. Full tables, no truncation.

---

## PROMPT P9 — Austria: Korean & Japanese volume brands

Same task, rules, and table format as P8 (incl. Bundesland and dealer-group columns), Austria, official locators only.

Brands in scope: **Hyundai, Kia, Toyota, Lexus, Suzuki, Mazda, Honda, Nissan, Mitsubishi, Subaru**.

Importer hints: Hyundai and Mitsubishi are imported by Denzel Group (denzel.at); Toyota by Toyota Austria (Frey Group); use hyundai.at, kia.at, toyota.at, mazda.at, suzuki.at, honda.at, nissan.at, mitsubishi-motors.at, subaru.at dealer locators.

Same two outputs per brand (TOTAL line + full table).

---

## PROMPT P10 — Austria: Chinese brands (all of them)

Same task, rules, and table format as P8, Austria.

Brands in scope: **MG, BYD, Omoda, Jaecoo, GWM (Great Wall/Ora/Wey), Leapmotor, Xpeng, BAIC, Dongfeng, Zeekr, Lynk & Co, Maxus, Hongqi, plus any other Chinese brand with an active authorized sales network in Austria**.

Note: MG in Austria runs via Denzel; BYD Austria launched via Denzel as well — capture the importer relationship per brand in one line before each table. If a brand has NO authorized network in Austria, state that in one line. The dealer-group column matters doubly here (CN brands recruit established groups).

---

## PROMPT P11 — Austria: remaining volume brands

Same task, rules, and table format as P8, Austria, official locators only, full enumeration.

Brands in scope: **Ford, Renault, Dacia, Alpine, Peugeot, Citroën, Opel, Fiat (incl. Fiat Professional), Jeep, Volvo**.

For Stellantis brands, one row per brand-outlet combination is fine; flag shared locations in a short final note. Same two outputs per brand.

---

## PROMPT P12 — Austria: premium brands

Same task, rules, and table format as P8, Austria.

Brands in scope: **Mercedes-Benz (Pkw; note Pappas and Wiesenthal networks), BMW, MINI, Land Rover, Jaguar, Alfa Romeo, smart, DS, plus niche brands with authorized networks**.

Same two outputs per brand (TOTAL line + full table).

---

## Quality bar (applies to every prompt)
- Official locator/importer sources ONLY; mark any exception with `(secondary source)`.
- Never invent an outlet. Never round counts. State enumeration gaps explicitly.
- Sales vs service-only distinction is the single most important field, dealer-group affiliation the second.
- Keep German diacritics (ä ö ü ß) exactly.
- Full tables, no truncation with "...and more".

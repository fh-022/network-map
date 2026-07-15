# Perplexity Prompt Pack AUSTRIA V2 (P8b–P12b) — source-first strategy

**Why v2:** The locator-based AT prompts failed (all major AT brand locators are dynamic JS), and under pressure the session began *reconstructing* plausible dealer tables from known group patterns — e.g., Porsche Inter Auto locations listed as Toyota dealers, which is impossible (PIA sells VW Group only). Perplexity's own follow-up analysis identified the right static sources; these prompts target them directly.

**Important: start a FRESH Perplexity thread for these.** The current thread contains fabricated tables that a continuation would build on.

**Every prompt below includes the same guard block — do not remove it.**

---

## GUARD BLOCK (included in every prompt)

> CRITICAL RULES: Only include a dealer row if you actually retrieved a document or page showing that dealer. Every row must cite the exact URL you retrieved (not a homepage, not a pattern like brand.at/dealer-name you didn't open). If a source cannot be retrieved, write "SOURCE NOT RETRIEVABLE: <url>" and STOP for that source — do NOT fill in dealers from memory, from known dealer-group location patterns, or from what is "likely". An empty table with an honest access note is a good result; a plausible reconstructed table is a failed result and will be discarded.

---

## PROMPT P8b — Porsche Bank Händlerverzeichnis (VW Group + multibrand)

Retrieve the Porsche Bank AG "Händlerverzeichnis" PDF for Austria (porschebank.at — the dealer directory listing all partner dealers with addresses; you located this document in a previous session). Enumerate EVERY entry in the document — expect roughly 200+ dealers across all 9 Bundesländer.

[GUARD BLOCK]

Output one markdown table:
| Dealer name | Legal company | Street | Postal code + City | Bundesland | Brands listed at this dealer (as stated in the document) | Source (PDF page/URL) |

Then one line: `TOTAL entries enumerated: <n> of <total in document>`. If the PDF is paginated and you cannot read all pages, state exactly which pages you covered.

---

## PROMPT P9b — Brand dealer association member lists (Toyota, Kia, Mazda, Nissan, Mercedes)

Austrian brand dealers are organized in official Händlerverbände (see voek-kfzverband.at/markenvereine). Retrieve the member lists (Mitgliederliste / Mitgliedsbetriebe) from these official association sites and enumerate every member dealer:

1. toyota-hv.at (Verein Österreichischer Toyota-Händler)
2. kia-hv.at (Verein österreichischer KIA Händlerbetriebe)
3. mazdahaendlerverband.at (Mazda Händlerverband)
4. Vereinigung der Nissan-Händler Österreichs (find via voek-kfzverband.at)
5. AVB — Verband österreichischer Mercedes-Benz Agenten (find via voek-kfzverband.at)

[GUARD BLOCK]

Per association, output:
`TOTAL <Brand> AT (association members): <n> (source URL, accessed <date>)`
| Dealer name | Legal company | Street | Postal code + City | Bundesland | Source URL |

---

## PROMPT P10b — Importer-owned retail & dealer-group networks (Denzel, Pappas, Wiesenthal, PIA)

Retrieve the official location directories ("Standorte") of Austria's dominant automotive retail groups and enumerate every location WITH the brands each location carries as stated on the group's own website:

1. denzel.at — Denzel Gruppe locations (Denzel is importer for Hyundai, Mitsubishi, MG, BYD and retails multiple brands)
2. pappas.at — Pappas Gruppe (Mercedes-Benz network, Austria-wide)
3. wiesenthal.at — Wiesenthal (Mercedes-Benz, Vienna region)
4. porscheinterauto.at / pia.at — Porsche Inter Auto locations (VW/Audi/SEAT/CUPRA/Škoda/Porsche ONLY — this group does not sell other brands)
5. eisner.at — Eisner Auto (Kärnten/Steiermark multi-brand)
6. autofrey.at — AutoFrey (Salzburg region)

[GUARD BLOCK]

Per group: one table
| Location name | Street | Postal code + City | Bundesland | Brands at this location (per group website) | Sales/Service as stated | Source URL |

---

## PROMPT P11b — Ayvens Austria dealer list PDF

Retrieve the Ayvens Austria partner/dealer list PDF (ayvens.com/de-at — driver-service documents section; a file like "ayvens-dealers-at" or Bestellleitfaden partner annex; the CH equivalent of this document yielded 200+ entries). Enumerate every dealer entry with the brand(s) noted per dealer.

[GUARD BLOCK]

| Dealer name | Street | Postal code + City | Bundesland | Brand(s) | Source (PDF URL + page) |
`TOTAL entries enumerated: <n>`

---

## PROMPT P12b — remaining brands via automobile.at brand index (secondary source, flagged)

For the following brands where no official static source exists, use the structured dealer index at automobile.at ("Händler mit Markenvertretung", brand-filtered pages like automobile.at/haendler/marken/<brand>.html): Ford, Renault, Dacia, Peugeot, Citroën, Opel, Fiat, Jeep, Volvo, Suzuki, Honda, Subaru, BMW, MINI, Land Rover, Jaguar, Alfa Romeo, plus Chinese brands (MG, BYD, Omoda/Jaecoo, Leapmotor, GWM, Maxus, BAIC).

[GUARD BLOCK — additionally: mark every row "(secondary source)" since automobile.at is a portal, not an official locator]

Per brand:
`TOTAL <Brand> AT (via automobile.at): <n> listed (secondary source, accessed <date>)`
| Dealer name | Street | Postal code + City | Bundesland | Source URL |

---

## Recommended run order & expectations

| Prompt | Expected yield | Confidence |
| --- | --- | --- |
| P8b Porsche Bank PDF | ~200 VW-Group/multibrand dealers | HIGH — static official document |
| P10b Group Standorte | ~80-120 locations incl. all Denzel/Pappas | HIGH — own websites |
| P9b Associations | Toyota/Kia/Mazda/Nissan/MB networks | MEDIUM-HIGH |
| P11b Ayvens PDF | ~150-200 multibrand | MEDIUM (retrievability unclear) |
| P12b automobile.at | fills remaining brands | MEDIUM (secondary source) |

Cross-brand overlaps between these sources are fine — the ingestion pipeline deduplicates by company + street.

# Nutrition Analytics Indonesia

**Data-Driven Prioritization of Child Nutrition Interventions in Indonesia Using Public Health, Education, and Socioeconomic Indicators**

A policy analytics and decision-support platform — not a one-off dashboard project — built to identify which Indonesian provinces should be prioritized for child-nutrition interventions (e.g. the Makan Bergizi Gratis program), using only real, publicly verifiable government data.

---

## Current Status

**Phase 0 complete (`v0.1.0`).** All 7 real datasets are fetched, contract-validated, and checksummed. `make validate`: 7/7 PASS. `pytest`: 18/18 PASS. Phase 1 has not started.

## Completed Milestones

- Production-style ingestion framework: config-driven for BPS sources, dedicated scripts where extraction genuinely differs (Tableau crosstab for stunting, GADM/BIG for boundaries)
- Every BPS variable id discovered and confirmed by live query — never guessed
- Per-dataset YAML data contracts enforced before any fetch counts as successful
- Province reference layer sourced from live statistical data (38 provinces, including the 2022 splits)
- Checksummed, append-only manifest + a generated (never hand-written) data inventory
- CI/CD: automated tests and contract validation on every push
- A governance document (`docs/known_limitations.md`) recording every structural limitation and the alternatives investigated and rejected for each

## Upcoming Milestone

**Phase 1 — Data Cleaning & Reconciliation**: reconcile the GADM province-boundary gap, standardize and merge all 6 non-geometry datasets into one analysis-ready table, and document every transformation in a cleaning notebook.

## Known Limitations

See `docs/known_limitations.md` for full detail. Headlines: GADM boundaries reflect 34 of Indonesia's 38 current provinces (missing the 2022 Papua splits); stunting has no scriptable source and requires a manual export to refresh; the education indicator uses a single age band (7-12) since BPS publishes no all-ages total.

---

## Phase 0 — Data Acquisition & Validation ✅

- Real BPS datasets: poverty rate, Human Development Index, population, school participation, household expenditure — all fetched via the BPS WebAPI with confirmed variable ids
- Stunting dataset: province-level child stunting prevalence (Kemenkes/TP2S), ingested from a manually-exported Tableau crosstab
- Province reference layer: single source of truth for province names, generated from live statistical data
- Validation framework: YAML data contracts enforced pre-fetch, schema + range + plausibility checks
- Manifest system: checksummed, append-only audit trail of every ingestion run
- CI/CD: GitHub Actions for tests and contract validation

## Phase 1 — Data Cleaning & Reconciliation

- Province reconciliation (resolving the GADM 34-vs-38 province gap before any geospatial join)
- Missing-value handling, decided and documented per dataset
- One merged province × year analytical dataset
- A cleaning notebook documenting every transformation against the real data

## Phase 2 — Feature Engineering

- Normalization of indicators onto comparable scales
- Indicator preparation for the priority-scoring framework
- Temporal consistency checks across datasets spanning different reference years

## Phase 3 — Nutrition Priority Index

- A transparent, documented scoring methodology
- A weighting framework across nutrition, economic, education, and development dimensions
- Sensitivity analysis on weighting choices (what-if scenarios)

## Phase 4 — Geospatial Analytics

- Province-level choropleth mapping
- Hotspot analysis for high-priority regions
- Regional clustering to identify province archetypes

## Phase 5 — Dashboard

- A Streamlit application (built and verified end-to-end as code)
- A Power BI implementation guide (specification for manual build, since `.pbix` files can't be authored or tested programmatically)

## Phase 6 — Policy Insights

- Intervention recommendations grounded in the priority index
- An executive summary for non-technical stakeholders
- A full policy report suitable for public-health or government audiences

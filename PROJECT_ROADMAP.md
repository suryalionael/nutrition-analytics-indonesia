# Nutrition Analytics Indonesia

**Data-Driven Prioritization of Child Nutrition Interventions in Indonesia Using Public Health, Education, and Socioeconomic Indicators**

A policy analytics and decision-support platform — not a one-off dashboard project — built to identify which Indonesian provinces should be prioritized for child-nutrition interventions (e.g. the Makan Bergizi Gratis program), using only real, publicly verifiable government data.

---

## Current Status

**Phase 3 in progress.** Phase 0 (`v0.1.0`) and Phase 1 are complete. Phase 2 (NPI methodology design) is complete — design documents only, no code. Phase 3 (`src/features/`, `src/scoring/`) is built and dry-run verified against real data: PCA loadings, variance explained, normalization diagnostics, and outlier review all computed (`docs/phase3_dry_run.md`); the missing-data policy is resolved (`docs/phase3_missing_data_decision.md`); validation procedures are designed but not yet executed (`docs/phase3_validation_design.md`). `pytest`: 37/37 PASS. **No province rankings, percentiles, or priority tiers exist yet** — publishing a ranking is a deliberately separate, not-yet-authorized step.

## Completed Milestones

- Production-style ingestion framework: config-driven for BPS sources, dedicated scripts where extraction genuinely differs (Tableau crosstab for stunting, GADM/BIG for boundaries)
- Every BPS variable id discovered and confirmed by live query — never guessed
- Per-dataset YAML data contracts enforced before any fetch counts as successful
- Province reference layer sourced from live statistical data (38 provinces, including the 2022 splits)
- Checksummed, append-only manifest + a generated (never hand-written) data inventory
- CI/CD: automated tests and contract validation on every push
- A governance document (`docs/known_limitations.md`) recording every structural limitation and the alternatives investigated and rejected for each
- Province reconciliation methodology covering 3 distinct gap types (aggregate rows, genuine BPS publication gaps, GADM geometry vintage) with a documented GADM crosswalk for Phase 4
- A single merged, validated `province × year` analytical table built without any imputation — missing values are real, documented BPS publication gaps, not estimated
- A defensible NPI methodology design: collinearity between `poverty_rate`/`ipm`/`expenditure_per_capita` (r up to 0.88) found and addressed via PCA rather than naive equal weighting; `stunting_rate` kept out of the weighted index as an outcome/validation variable rather than an input, to avoid circularity
- A working, tested scoring pipeline (`src/features/`, `src/scoring/`) producing real per-province diagnostics (86.0% PCA variance explained, confirmed real outlier provinces) without producing a published ranking

## Upcoming Milestone

**Validation execution**: run the procedures designed in `docs/phase3_validation_design.md` (outcome correlation, rank stability, weight sensitivity, leave-one-indicator-out) against the real pipeline, then — pending that review — authorize computing and publishing an actual province ranking.

## Known Limitations

See `docs/known_limitations.md`, `docs/province_reconciliation.md`, and `docs/phase3_missing_data_decision.md` for full detail. Headlines: GADM boundaries reflect 34 of Indonesia's 38 current provinces (missing the 2022 Papua splits); stunting has no scriptable source and requires a manual export to refresh; the education indicator uses a single age band (7-12) since BPS publishes no all-ages total; `population` and `participation_rate` are missing for the 4 newest Papua provinces because BPS has not yet republished those two series for them (handled via per-province dimension-weight renormalization, not imputation).

---

## Phase 0 — Data Acquisition & Validation ✅

- Real BPS datasets: poverty rate, Human Development Index, population, school participation, household expenditure — all fetched via the BPS WebAPI with confirmed variable ids
- Stunting dataset: province-level child stunting prevalence (Kemenkes/TP2S), ingested from a manually-exported Tableau crosstab
- Province reference layer: single source of truth for province names, generated from live statistical data
- Validation framework: YAML data contracts enforced pre-fetch, schema + range + plausibility checks
- Manifest system: checksummed, append-only audit trail of every ingestion run
- CI/CD: GitHub Actions for tests and contract validation

## Phase 1 — Data Cleaning & Reconciliation ✅

- Province reconciliation (resolving the GADM 34-vs-38 province gap and 2 genuine BPS publication gaps, documented in `docs/province_reconciliation.md`)
- Missing-value handling, decided and documented per dataset (`docs/missing_data_report.md`) — never imputed
- One merged province × year analytical dataset (`data/processed/merged_provincial_indicators.csv`)
- A cleaning notebook documenting every transformation against the real data (`notebooks/02_cleaning.ipynb`, executed)

## Phase 2 — Feature Engineering & NPI Methodology Design ✅

- Indicator audit grounding the design in real correlations and gaps, not assumptions (`docs/phase2_indicator_audit.md`)
- A 2-input-dimension framework (Socioeconomic Vulnerability, Education Access) with stunting as a reported outcome layer and population as a reach modifier, not 4 naive additive dimensions (`docs/phase2_framework_design.md`)
- A hybrid weighting methodology — PCA within the collinear vulnerability trio, equal weighting across top-level dimensions — compared against equal/expert/pure-PCA alternatives (`docs/phase2_weighting_options.md`)
- A sensitivity-analysis design and technical architecture for `src/features/`/`src/scoring/` (`docs/phase2_sensitivity_design.md`, `docs/phase2_technical_design.md`)

## Phase 3 — Nutrition Priority Index (in progress)

- Missing-data policy resolved: renormalize dimension weights for the 4 partial-coverage provinces rather than exclude or fabricate (`docs/phase3_missing_data_decision.md`)
- `src/features/` (directionality alignment, normalization, missing-value policy) and `src/scoring/` (PCA composite, NPI combination) built and tested (13 new tests)
- Dry-run verified against real data: PCA loadings, 86.0% variance explained, normalization diagnostics, outlier review — no rankings produced (`docs/phase3_dry_run.md`)
- Validation procedures fully specified against the real pipeline, not yet executed (`docs/phase3_validation_design.md`)
- **Not yet done:** running validation, computing percentiles/tiers, publishing any ranking

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

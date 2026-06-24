# Data-Driven Prioritization of Child Nutrition Interventions in Indonesia

**Status: Phase 5 complete — spatial analysis confirms real, significant geographic clustering**

Phase 0 (data acquisition, `v0.1.0`) through Phase 4 (rankings and priority tiers — [data/processed/npi_rankings.csv](data/processed/npi_rankings.csv)) are done. Phase 5 resolved the GADM 34-vs-38 geometry gap with a real, distinct-geometry source for all 38 current provinces ([docs/phase5_geometry_reconciliation.md](docs/phase5_geometry_reconciliation.md)) and ran global/local spatial autocorrelation plus a regional comparison: **global Moran's I = 0.622 (p = 0.001), and all 6 Papua-region provinces form one statistically significant High-High LISA cluster** — independent confirmation, via a different statistical method, of the same pattern Phase 4's ranking already surfaced. Eastern Indonesia's mean NPI is 2.5× Western's (ANOVA p = 2.8×10⁻⁸). Full results: [docs/phase5_spatial_results.md](docs/phase5_spatial_results.md). See [docs/known_limitations.md](docs/known_limitations.md) and [docs/province_reconciliation.md](docs/province_reconciliation.md) for structural limitations, and [docs/phase4_ranking_results.md](docs/phase4_ranking_results.md) for the important rank-vs-tier-stability finding carried into this phase.

A policy-analytics decision-support project ranking Indonesian provinces by child-nutrition-intervention priority (e.g. for programs like Makan Bergizi Gratis), using public health, education, and socioeconomic indicators. This is not a dashboard project — it's an analytics engineering foundation: data contracts, provenance, and validation come before any analysis.

See [PROJECT_ROADMAP.md](PROJECT_ROADMAP.md) for the full phase-by-phase plan (Phase 0 through Phase 6) and current status.

## No Synthetic Data — Ever

Every dataset in this repository is real and publicly verifiable, sourced from BPS (Statistics Indonesia), Kemenkes/TP2S, and GADM/BIG. If a source is unreachable, authentication fails, or a source's structure changes, ingestion **fails loudly and exits non-zero** — it never falls back to mock, generated, or cached-fake data. See [docs/data_inventory.md](docs/data_inventory.md) for the full audit trail of what was actually fetched, when, and from where.

## Data Sources

| Dataset | Source | Access method |
|---|---|---|
| Poverty rate by province | BPS | WebAPI (requires free API key) |
| Human Development Index (IPM) | BPS | WebAPI |
| Population by province | BPS | WebAPI |
| School participation rate (APS/APK/APM) | BPS | WebAPI |
| Household per-capita expenditure | BPS | WebAPI |
| Child stunting prevalence | Kemenkes / TP2S | Tableau Public dashboard (manual crosstab export — automated scrape is broken, see known_limitations.md) |
| Province administrative boundaries | GADM (default) / BIG (optional, manual) | Direct download |

Full provenance — source URLs, publication dates, checksums, validation status — is generated from real ingestion runs in [docs/data_inventory.md](docs/data_inventory.md). It is never hand-written. Structural limitations and the alternative sources investigated and rejected for each are in [docs/known_limitations.md](docs/known_limitations.md).

## Repository Structure

```
nutrition-analytics-indonesia/
├── config/              dataset configs (datasets.yml, metadata.yml)
├── data/{raw,interim,processed,external}/   never committed; always re-fetched
├── docs/
│   ├── data_inventory.md          generated audit trail
│   ├── data_contracts/            per-dataset YAML schema contracts
│   ├── known_limitations.md       structural limitations + alternatives investigated
│   ├── province_reconciliation.md GADM 34-vs-38 + BPS publication-gap methodology (Phase 0/1)
│   ├── missing_data_report.md     generated per-dataset missingness profile
│   └── phase2_*.md phase3_*.md phase4_*.md phase5_*.md   per-phase design/results docs
├── notebooks/           01_data_audit (placeholder) · 02_cleaning (Phase 1, executed) · 03-05 (placeholders; phase 6+)
├── src/
│   ├── ingestion/       fetch scripts + orchestrator (incl. fetch_geo_boundaries.py --source big_mirror, Phase 5)
│   ├── reference/       province name standardization (single source of truth) + GADM crosswalk
│   ├── cleaning/        standardize.py, profile_missing.py, merge.py (Phase 1)
│   ├── features/        directionality, normalization, missing-value policy (Phase 3)
│   ├── scoring/         PCA/single-indicator composites, NPI, ranking, validation (Phases 3-4)
│   ├── geospatial/      boundaries, spatial join, Moran's I/LISA, regions, maps (Phase 5)
│   ├── validation/      data-contract enforcement
│   ├── utils/           HTTP retry, config, provenance/manifest
│   └── visualization/   placeholder for later phases
├── tests/               unit tests, no real network calls
├── .github/workflows/   CI: tests + contract validation
├── reports/maps/        generated spatial diagnostic maps (Phase 5)
└── dashboard/           placeholder for later phases
```

## Setup & Reproducibility

```bash
git clone <repo>
cd nutrition-analytics-indonesia
python -m venv .venv && source .venv/bin/activate
make install
cp .env.example .env
# Sign up free at https://webapi.bps.go.id/, create an application, paste the App ID into .env as BPS_API_KEY
# Manually export the stunting crosstab (see known_limitations.md §3) to data/external/stunting_tableau_crosstab_2024.xlsx
make fetch       # downloads the 6 scriptable datasets into data/raw/, builds the manifest
python -m src.ingestion.fetch_stunting_ssgi --manual-xlsx data/external/stunting_tableau_crosstab_2024.xlsx
make validate      # re-checks already-fetched data against docs/data_contracts/
make inventory     # regenerates docs/data_inventory.md from the real manifest
make clean-data    # profiles missingness (docs/missing_data_report.md) and builds data/processed/merged_provincial_indicators.csv
make rankings      # builds data/processed/npi_rankings.csv (Phase 4)
make fetch-boundaries  # downloads real, distinct 38-province geometry (Phase 5; ~500MB raw download)
make spatial       # builds data/processed/npi_spatial.geojson, Moran's I/LISA, regional tests, maps (Phase 5)
make test          # runs the unit test suite (no network required)
```

The 5 BPS-sourced datasets (poverty, IPM, population, education, expenditure) require your own free `BPS_API_KEY` — the BPS WebAPI rejects every request without one, including read-only list endpoints, and there is no scriptable way around that. `config/datasets.yml` already has the real, confirmed var ids (see [docs/known_limitations.md](docs/known_limitations.md) §2 for how they were found and verified) — `discover_bps_vars.py` is there if you ever need to re-derive one. Boundaries (GADM) work without any key. Stunting requires a manual crosstab export placed at `data/external/` and ingested with `--manual-xlsx`; see [docs/known_limitations.md](docs/known_limitations.md) §3 — re-fetching a future year means repeating that export.

## Roadmap

See [PROJECT_ROADMAP.md](PROJECT_ROADMAP.md) for the full Phase 0–6 plan.

- **Phase 0 (complete, `v0.1.0`):** scaffold, data contracts, province reference layer, provenance/manifest, validation framework, CI/CD, inventory generation, and all 7 real datasets fetched + contract-validated.
- **Phase 1 (complete):** province reconciliation (3 distinct gap types documented in `docs/province_reconciliation.md`), per-dataset cleaning (`src/cleaning/standardize.py`), a missing-data report (`docs/missing_data_report.md`), and one merged, validated `province × year` table (`data/processed/merged_provincial_indicators.csv`), all documented in `notebooks/02_cleaning.ipynb`.
- **Phase 2 (complete, design only):** NPI methodology design — indicator audit, dimensional framework, weighting methodology comparison, sensitivity-analysis design, technical architecture (`docs/phase2_*.md`). No code.
- **Phase 3 (complete):** `src/features/` and `src/scoring/` built, dry-run verified, validated (`docs/phase3_validation_results.md`), and the primary methodology empirically chosen via a 4-way comparison (`docs/phase3_methodology_comparison.md`, `docs/phase3_final_methodology_decision.md`).
- **Phase 4 (complete):** province rankings, percentiles, and priority tiers published (`data/processed/npi_rankings.csv`), with 4 tiering methods compared on real evidence and tier-stability explicitly flagged as the weaker link compared to rank stability (`docs/phase4_ranking_design.md`, `docs/phase4_ranking_results.md`).
- **Phase 5 (complete):** geometry reconciliation with a real distinct-geometry source for all 38 provinces, spatial join (`data/processed/npi_spatial.geojson`), global/local Moran's I, regional disparity testing, spatial robustness checks, and 4 maps (`reports/maps/`) — full results in `docs/phase5_spatial_results.md`.
- **Phase 6+ (not started):** the dashboard and policy insights.

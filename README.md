# Data-Driven Prioritization of Child Nutrition Interventions in Indonesia

**Status: Phase 0 complete (v0.1.0) — all 7 datasets fetched and contract-validated**

Phase 0A (scaffold, data contracts, province reference layer, manifest/provenance system, validation framework, CI/CD, inventory generation) and Phase 0B (real dataset acquisition) are both done: all 7 datasets — poverty, IPM, population, education, expenditure, stunting, and province boundaries — are real, fetched, and pass their data contracts. `make validate` and the full test suite pass. See [docs/known_limitations.md](docs/known_limitations.md) for the structural limitations that remain (BPS variable choices, the manual stunting export, GADM's province vintage) even though ingestion itself is complete. Phase 1 (cleaning) has not started.

A policy-analytics decision-support project ranking Indonesian provinces by child-nutrition-intervention priority (e.g. for programs like Makan Bergizi Gratis), using public health, education, and socioeconomic indicators. This is not a dashboard project — it's an analytics engineering foundation: data contracts, provenance, and validation come before any analysis.

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
│   └── data_contracts/            per-dataset YAML schema contracts
├── notebooks/           01_data_audit ... 05_geospatial (placeholders; phases 1+)
├── src/
│   ├── ingestion/       fetch scripts + orchestrator
│   ├── reference/       province name standardization (single source of truth)
│   ├── validation/      data-contract enforcement
│   ├── utils/           HTTP retry, config, provenance/manifest
│   └── cleaning/ features/ scoring/ visualization/   placeholders for later phases
├── tests/               unit tests, no real network calls
├── .github/workflows/   CI: tests + contract validation
└── reports/ dashboard/  placeholders for later phases
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
make validate    # re-checks already-fetched data against docs/data_contracts/
make inventory   # regenerates docs/data_inventory.md from the real manifest
make test        # runs the unit test suite (no network required)
```

The 5 BPS-sourced datasets (poverty, IPM, population, education, expenditure) require your own free `BPS_API_KEY` — the BPS WebAPI rejects every request without one, including read-only list endpoints, and there is no scriptable way around that. `config/datasets.yml` already has the real, confirmed var ids (see [docs/known_limitations.md](docs/known_limitations.md) §2 for how they were found and verified) — `discover_bps_vars.py` is there if you ever need to re-derive one. Boundaries (GADM) work without any key. Stunting requires a manual crosstab export placed at `data/external/` and ingested with `--manual-xlsx`; see [docs/known_limitations.md](docs/known_limitations.md) §3 — re-fetching a future year means repeating that export.

## Roadmap

- **Phase 0 (complete, v0.1.0):** scaffold, data contracts, province reference layer, provenance/manifest, validation framework, CI/CD, inventory generation, and all 7 real datasets fetched + contract-validated.
- **Phase 1 (not started):** province reconciliation, cleaning, missing-value handling, a merged analytical dataset, and a cleaning notebook. No scoring, ranking, modeling, or dashboard yet.

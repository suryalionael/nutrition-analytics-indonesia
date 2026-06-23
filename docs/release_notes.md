# Release Notes

## v0.1.0 — Phase 0 complete: Data Foundation, Governance & Real Dataset Acquisition

**Status:** all 7 datasets real, fetched, and contract-validated. `make validate` and
the full test suite (18/18) pass. No synthetic, mocked, or fabricated data anywhere in
the pipeline.

### What's included

- Repository scaffold matching the project's required layout (`config/`, `data/`,
  `docs/`, `notebooks/`, `src/`, `tests/`, `reports/`, `dashboard/`).
- Per-dataset YAML data contracts (`docs/data_contracts/`) enforced before any fetch is
  marked successful.
- A province reference layer (`src/reference/`) sourced from live BPS statistical data
  (not a stale metadata endpoint — see below), the single source of truth every dataset
  standardizes province names against.
- A config-driven BPS ingestion framework (`config/datasets.yml` +
  `fetch_bps_dataset.py`) covering poverty, IPM, population, education, and
  expenditure, plus dedicated scripts for stunting and province boundaries where the
  extraction mechanism genuinely differs.
- A checksummed, append-only manifest (`data/raw/_manifest.jsonl`) and a generated
  `docs/data_inventory.md` — never hand-written, always derived from what was actually
  fetched.
- CI (`.github/workflows/`): tests on every push, contract validation with an optional
  `BPS_API_KEY` secret.
- `docs/known_limitations.md`: every structural limitation and the alternatives
  investigated and rejected for each, as permanent project governance.

### Dataset summary

| Dataset | Source | Vintage | Rows | Access method |
|---|---|---|---|---|
| Poverty rate | BPS (var 192) | 2025 (Sept) | 78 | WebAPI |
| Human Development Index | BPS (var 494) | 2024 | 117 | WebAPI |
| Population | BPS (var 1886) | 2020 | 105 | WebAPI |
| School participation (age 7-12) | BPS (var 301) | 2023 | 105 | WebAPI |
| Household per-capita expenditure | BPS (var 416) | 2025 | 110 | WebAPI |
| Child stunting prevalence | Kemenkes/TP2S | 2024 | 38 | Manual Tableau crosstab export |
| Province boundaries | GADM | current | 34 provinces | Direct download |

Full per-dataset provenance (URLs, checksums, fetch timestamps) is in
`docs/data_inventory.md`, generated from the real manifest.

### Notable fixes during Phase 0B

- `discover_bps_vars.py` was returning 0 results for every search — root cause was
  missing pagination (BPS's var list is 1699 entries across 170 fixed-size pages), not
  an auth or filtering bug.
- The BPS dynamic-table parser originally tried to split composite `datacontent` keys
  by substring position, which silently produced zero rows against real data. Fixed by
  constructing keys from known dimension values instead of parsing them.
- The province reference layer was sourcing from BPS's `/domain/type/prov/` endpoint,
  which returns a stale 34-province scheme missing the 2022 Papua splits. Fixed by
  sourcing from a live statistical variable's region list instead (38 provinces,
  matches every other real dataset in this project).
- `TableauScraper` was removed from `requirements.txt` (unmaintained, confirmed broken
  against the current dashboard frontend); a manual crosstab export + `--manual-xlsx`
  is now the supported path for stunting.

### Known limitations carried forward (not blockers, see `docs/known_limitations.md`)

- GADM boundaries reflect 34 provinces, not the current 38 (missing the 2022 Papua
  splits) — must be reconciled before geospatial analysis treats provinces as join
  keys.
- Stunting has no scriptable source; re-fetching a future year requires repeating the
  manual Tableau export.
- The education dataset uses the 7-12 age-group APS series (no all-ages total exists)
  — a documented scope decision, revisit in Phase 1 if needed.

### Recommended tag

`git tag v0.1.0` — all validation gates pass; this is a clean point to mark Phase 0 as
done before Phase 1 (cleaning) begins. Not created automatically; tagging is left to
you to run (`git tag -a v0.1.0 -m "Phase 0 complete: all 7 datasets real, fetched, and validated"`).

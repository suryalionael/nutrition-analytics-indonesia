"""Fetches Indonesia province administrative boundaries.

Two sources, by design:

- GADM (default, scriptable): https://gadm.org -- free, no registration, derived from
  official national mapping agency data. Confirmed reachable and downloadable without
  auth during Phase 0 research. Used as the default so `make fetch` is fully
  unattended and reproducible end-to-end.
- BIG / Ina-Geoportal (--source big, optional upgrade): https://tanahair.indonesia.go.id
  is Indonesia's own official geospatial agency and is the more authoritative source,
  but requires a free human registration + manual download through their portal, which
  cannot be scripted. When chosen, this script only validates a file the operator has
  already placed by hand -- it never invents one.

Usage:
    python -m src.ingestion.fetch_geo_boundaries            # GADM, fully scripted
    python -m src.ingestion.fetch_geo_boundaries --source big   # validates a manually-placed BIG file
"""

import argparse
import json
import logging
from pathlib import Path

import pandas as pd

from src.utils.config import RAW_DIR
from src.utils.http import download_file
from src.utils.provenance import timestamped_path, write_manifest_entry
from src.validation.contracts import Contract, validate

log = logging.getLogger(__name__)

GADM_URL = "https://geodata.ucdavis.edu/gadm/gadm4.1/json/gadm41_IDN_1.json"
BIG_MANUAL_DIR = RAW_DIR / "boundaries" / "big"


def fetch_gadm() -> tuple[pd.DataFrame, Path, str]:
    out_path = timestamped_path(RAW_DIR / "boundaries", "boundaries_gadm", "geojson")
    download_file(GADM_URL, out_path, min_size_bytes=100_000)

    with open(out_path) as f:
        geojson = json.load(f)

    df = pd.json_normalize([feat["properties"] for feat in geojson["features"]])
    name_col = next((c for c in df.columns if c.upper() in ("NAME_1", "PROVINCE", "PROVINSI")), None)
    if name_col is None:
        raise RuntimeError(f"Could not find a province-name property in GADM GeoJSON. Properties found: {list(df.columns)}")
    df = df.rename(columns={name_col: "province_name"})[["province_name"]]
    return df, out_path, GADM_URL


def validate_manual_big_file() -> tuple[pd.DataFrame, Path, str]:
    candidates = sorted(BIG_MANUAL_DIR.glob("*.geojson")) + sorted(BIG_MANUAL_DIR.glob("*.json"))
    if not candidates:
        raise FileNotFoundError(
            f"No BIG boundary file found in {BIG_MANUAL_DIR}. Register at "
            "https://tanahair.indonesia.go.id/portal-web/unduh, download the province "
            "(level-1) RBI shapefile/GeoJSON by hand, convert to GeoJSON if needed, and "
            f"place it in {BIG_MANUAL_DIR} before re-running with --source big."
        )
    file_path = candidates[0]
    with open(file_path) as f:
        geojson = json.load(f)
    df = pd.json_normalize([feat["properties"] for feat in geojson["features"]])
    name_col = next((c for c in df.columns if "nama" in c.lower() or "prov" in c.lower()), None)
    if name_col is None:
        raise RuntimeError(f"Could not find a province-name property in BIG file. Properties found: {list(df.columns)}")
    df = df.rename(columns={name_col: "province_name"})[["province_name"]]
    return df, file_path, "https://tanahair.indonesia.go.id/portal-web/unduh (manually downloaded)"


def main() -> int:
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", choices=["gadm", "big"], default="gadm")
    args = parser.parse_args()

    try:
        if args.source == "gadm":
            df, out_path, source_url = fetch_gadm()
            source_name = "GADM (derived from official boundary data)"
        else:
            df, out_path, source_url = validate_manual_big_file()
            source_name = "BIG (Badan Informasi Geospasial) Ina-Geoportal"

        validate(df, Contract.load("boundaries"))
    except Exception:
        log.exception("Boundary ingestion failed (source=%s)", args.source)
        return 1

    write_manifest_entry(
        dataset="boundaries",
        dataset_version=args.source,
        source_name=source_name,
        source_url=source_url,
        file_path=out_path,
        rows=len(df),
        columns=len(df.columns),
        fetch_status="success",
        validation_status="passed",
    )
    log.info("Fetched boundaries (%s) -> %s (%d provinces)", args.source, out_path, len(df))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

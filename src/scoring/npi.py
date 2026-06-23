"""Combines the Socioeconomic Vulnerability composite (src/scoring/pca_composite.py)
and the Education Access dimension into the Nutrition Priority Index, per
docs/phase2_framework_design.md and docs/phase2_weighting_options.md, applying the
missing-data policy from docs/phase3_missing_data_decision.md.

Deliberately produces only a continuous score and diagnostics in this module --
NOT a sorted ranking, percentile, or priority tier. Turning the score into an
ordered ranking is an explicitly separate, not-yet-authorized step (see
docs/phase3_dry_run.md); building that here would make this module's mere existence
produce a ranking artifact every time it runs.
"""

import yaml

import pandas as pd

from src.features.directionality import align_to_higher_is_worse, load_directionality_config
from src.features.missing_value_policy import completeness_flag, renormalize_weights_per_row
from src.features.normalize import min_max_scale
from src.scoring.pca_composite import fit_pca_composite
from src.utils.config import CONFIG_DIR

NPI_WEIGHTS_PATH = CONFIG_DIR / "npi_weights.yml"

SOCIOECONOMIC_COLUMNS = ["poverty_rate", "ipm", "expenditure_per_capita"]
EDUCATION_COLUMN = "participation_rate"


def load_npi_weights(path=NPI_WEIGHTS_PATH) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def compute_npi(merged_df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """merged_df: data/processed/merged_provincial_indicators.csv, loaded.

    Returns (result_df, diagnostics). result_df has one row per province: the two
    dimension scores, the combined npi score, the reach-modifier metric, and the
    data_completeness flag -- no rank, percentile, or tier column.
    """
    npi_config = load_npi_weights()
    directionality_config = load_directionality_config()

    aligned = align_to_higher_is_worse(merged_df, directionality_config)

    socio_input, socio_diag = min_max_scale(aligned, SOCIOECONOMIC_COLUMNS)
    edu_input, edu_diag = min_max_scale(aligned, [EDUCATION_COLUMN])

    pca_config = npi_config["socioeconomic_vulnerability_method"]
    socioeconomic_vulnerability, pca_diag = fit_pca_composite(
        socio_input, SOCIOECONOMIC_COLUMNS, n_components=pca_config["n_components"]
    )

    # Rescale the PCA composite to [0, 1] for interpretability alongside education_access,
    # which is already on a [0, 1] scale from min_max_scale.
    socioeconomic_vulnerability, socio_pca_scale_diag = min_max_scale(
        pd.DataFrame({"socioeconomic_vulnerability": socioeconomic_vulnerability}), ["socioeconomic_vulnerability"]
    )
    socioeconomic_vulnerability = socioeconomic_vulnerability["socioeconomic_vulnerability"]

    dimension_scores = pd.DataFrame(
        {
            "socioeconomic_vulnerability": socioeconomic_vulnerability,
            "education_access": edu_input[EDUCATION_COLUMN],
        },
        index=merged_df.index,
    )

    weights = npi_config["dimension_weights"]
    effective_weights, npi = renormalize_weights_per_row(dimension_scores, weights)
    completeness = completeness_flag(dimension_scores, weights)

    result = pd.DataFrame(
        {
            "province": merged_df["province"],
            "socioeconomic_vulnerability": dimension_scores["socioeconomic_vulnerability"],
            "education_access": dimension_scores["education_access"],
            "npi": npi,
            "data_completeness": completeness,
            "estimated_children_affected": merged_df["population"] * merged_df["stunting_rate"] / 100.0,
            "stunting_rate": merged_df["stunting_rate"],
            "stunting_category": merged_df["stunting_category"],
        }
    )

    diagnostics = {
        "normalization": {**socio_diag, **edu_diag},
        "pca": pca_diag,
        "effective_weights_sample": effective_weights,
    }
    return result, diagnostics

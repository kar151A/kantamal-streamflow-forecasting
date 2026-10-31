"""Rank river subbasins using the Gandak fallback-bargaining method.

This is a separate subbasin-prioritization analysis, not an LSTM input.
Run from the repository root:
    python -m src.fallback_bargaining --input data/gandak/gandak_gspi_subbasin.csv
"""

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


# These column names come from the professor's Gandak script.
INDICATORS = {
    "forest_pct": "forest_inv",
    "slope30plus_pct": "slope30plus_norm",
    "bd34_pct": "bd34_norm",
    "agri_pct": "agri_norm",
}


def minmax_norm(series):
    """Convert a numeric column to 0..1, as in the original script."""
    minimum = series.min()
    maximum = series.max()
    if maximum == minimum:
        return pd.Series(0.0, index=series.index)
    return (series - minimum) / (maximum - minimum)


def prioritize_subbasins(df):
    """Return (smallest fallback level, accepted IDs, full ranked table).

    An accepted subbasin has rank <= k for ALL four indicators.
    Rank 1 means the highest priority within each indicator.
    """
    required = ["subbasin", *INDICATORS]
    missing = [name for name in required if name not in df.columns]
    if missing:
        raise ValueError(f"Missing required CSV columns: {', '.join(missing)}")
    if df.empty:
        raise ValueError("The input CSV contains no subbasins.")

    ranked = df.copy().reset_index(drop=True)
    if ranked["subbasin"].isna().any():
        raise ValueError("The subbasin column contains missing IDs.")
    # Keep IDs as strings: an ID such as '0012' should not become 12.
    ranked["subbasin"] = ranked["subbasin"].astype(str).str.strip()
    if (ranked["subbasin"] == "").any() or ranked["subbasin"].duplicated().any():
        raise ValueError("Subbasin IDs must be nonempty and unique.")

    for column in INDICATORS:
        try:
            ranked[column] = pd.to_numeric(ranked[column], errors="raise")
        except (ValueError, TypeError) as exc:
            raise ValueError(f"{column} must contain numeric percentages.") from exc
        if not np.isfinite(ranked[column].to_numpy(dtype=float)).all():
            raise ValueError(f"{column} contains missing or infinite values.")
        if not ranked[column].between(0, 100).all():
            raise ValueError(f"{column} must contain percentages between 0 and 100.")

    # Less forest is treated as higher priority, as in the original code.
    ranked["forest_inv"] = 1 - minmax_norm(ranked["forest_pct"])
    for column, normalized in INDICATORS.items():
        if column != "forest_pct":
            ranked[normalized] = minmax_norm(ranked[column])

    rank_columns = []
    for normalized in INDICATORS.values():
        rank_column = normalized + "_rank"
        ranked[rank_column] = ranked[normalized].rank(
            method="min", ascending=False
        ).astype(int)
        rank_columns.append(rank_column)

    # The first level that accepts anyone is min(max(rank per indicator)).
    # We use the same step-by-step search as the professor's original code.
    rank_matrix = ranked[rank_columns].to_numpy()
    for k in range(1, len(ranked) + 1):
        accepted_mask = np.all(rank_matrix <= k, axis=1)
        if np.any(accepted_mask):
            ranked["accepted"] = accepted_mask
            ranked["worst_indicator_rank"] = rank_matrix.max(axis=1)
            accepted_ids = ranked.loc[accepted_mask, "subbasin"].tolist()
            return k, accepted_ids, ranked

    # This should not happen with valid, nonempty data and complete ranks.
    raise RuntimeError("No fallback level succeeded. Check the input data.")


def main():
    parser = argparse.ArgumentParser(
        description="Prioritize subbasins using four-indicator fallback bargaining."
    )
    parser.add_argument("--input", required=True, help="Path to subbasin CSV")
    parser.add_argument(
        "--output", default="results/gandak_fallback_ranking.csv",
        help="Where to save the full ranking table",
    )
    args = parser.parse_args()

    df = pd.read_csv(args.input, dtype={"subbasin": str})
    level, accepted, ranked = prioritize_subbasins(df)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    ranked.to_csv(output_path, index=False)

    print(f"First successful fallback level: k = {level}")
    print("Accepted subbasins: " + ", ".join(accepted))
    print(f"Full ranking saved to: {output_path}")


if __name__ == "__main__":
    main()

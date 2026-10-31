# Gandak fallback bargaining — subbasin prioritization

This is an **independent research module** in the Kantamal streamflow forecasting repository. It does **not** change the LSTM, BiLSTM, or Transformer models and does not yet rank Kantamal subbasins. The original code and notebook were supplied for the Gandak basin.

## What it does (in simple English)

1. Read one CSV row for each subbasin.
2. Turn the four percentage indicators into values from 0 to 1 (min–max normalization).
3. Reverse the forest score: **less forest = higher priority** under the supplied method.
4. Rank subbasins separately for each indicator. Rank 1 means highest priority; tied values share the minimum rank.
5. Start with fallback level `k = 1`. Accept a subbasin only when **all four ranks are at most `k`**.
6. If no subbasin passes, try `k = 2`, then `k = 3`, and so on. Stop at the **first** successful level.
7. Save every subbasin's original values, normalized values, ranks, and whether it was accepted.

The columns are exactly those used by the professor's script:

| CSV column | Interpretation in this code |
| --- | --- |
| `subbasin` | Unique subbasin ID |
| `forest_pct` | Forest percentage; lower values get higher priority |
| `slope30plus_pct` | Percentage with steep slope; higher values get higher priority |
| `bd34_pct` | Soil-related percentage; higher values get higher priority **under the supplied code**. Confirm its precise scientific meaning before presenting. |
| `agri_pct` | Agricultural land percentage; higher values get higher priority |

**Research caution:** These are the priorities assumed by the supplied code. The ranking is not a validated flood-risk or erosion-risk score. Scientific justification and independent validation are still required.

## How to run

From the repository root, with Python, pandas and NumPy installed:

```bash
python -m src.fallback_bargaining --input data/gandak/gandak_gspi_subbasin.csv
```

The script prints the smallest successful fallback level and selected subbasin IDs. It also writes:

`results/gandak_fallback_ranking.csv`

You can choose a different output location:

```bash
python -m src.fallback_bargaining --input path/to/subbasins.csv --output results/my_ranking.csv
```

To run tests (no real dataset needed):

```bash
python -m unittest discover -s tests -p 'test_fallback_bargaining.py' -v
```

## Example for understanding (invented data, not Gandak measurements)

Suppose the four ranks of subbasin A are `[1, 2, 2, 1]`.

- At `k = 1`, A fails because two ranks are 2.
- At `k = 2`, A passes because **every rank is 2 or less**.

If A is the first subbasin to satisfy all conditions, the method stops at `k = 2`.

## Differences from the supplied script

The core normalization, forest inversion, rank method, and fallback rule are unchanged. This version also validates input columns, checks for missing/invalid percentages and duplicate IDs, keeps IDs as strings, saves a full results table, and has automated tests. It does not create or guess real Gandak data.

## Next research step

Place the actual `gandak_gspi_subbasin.csv` file in `data/gandak/`, run the script, inspect the ranking, and check the meaning and justification of `bd34_pct` with the professor. For Kantamal subbasin prioritization, we would first need correctly delineated Kantamal subbasins and the same four indicators measured for each one.

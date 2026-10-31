"""Tests for the Gandak subbasin-prioritization module."""

import unittest

import pandas as pd

from src.fallback_bargaining import minmax_norm, prioritize_subbasins


class FallbackBargainingTests(unittest.TestCase):
    def test_first_successful_level_and_accepted_subbasin(self):
        data = pd.DataFrame({
            "subbasin": ["A", "B", "C", "D"],
            "forest_pct": [10, 20, 50, 90],
            "slope30plus_pct": [80, 100, 30, 10],
            "bd34_pct": [70, 40, 100, 20],
            "agri_pct": [90, 30, 60, 10],
        })
        level, accepted, ranked = prioritize_subbasins(data)
        self.assertEqual(level, 2)
        self.assertEqual(accepted, ["A"])
        self.assertEqual(ranked.loc[0, "worst_indicator_rank"], 2)
        self.assertEqual(ranked["accepted"].tolist(), [True, False, False, False])

    def test_ties_can_select_multiple_subbasins(self):
        data = pd.DataFrame({
            "subbasin": ["001", "002"],
            "forest_pct": [50, 50],
            "slope30plus_pct": [10, 10],
            "bd34_pct": [20, 20],
            "agri_pct": [30, 30],
        })
        level, accepted, _ = prioritize_subbasins(data)
        self.assertEqual(level, 1)
        self.assertEqual(accepted, ["001", "002"])

    def test_constant_column_normalizes_to_zero(self):
        self.assertEqual(minmax_norm(pd.Series([7, 7])).tolist(), [0.0, 0.0])

    def test_missing_column_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Missing required"):
            prioritize_subbasins(pd.DataFrame({"subbasin": [1]}))

    def test_missing_percentages_are_rejected(self):
        data = pd.DataFrame({
            "subbasin": ["A"],
            "forest_pct": [None],
            "slope30plus_pct": [20],
            "bd34_pct": [30],
            "agri_pct": [40],
        })
        with self.assertRaisesRegex(ValueError, "missing or infinite"):
            prioritize_subbasins(data)

    def test_duplicate_ids_are_rejected(self):
        data = pd.DataFrame({
            "subbasin": ["A", "A"],
            "forest_pct": [20, 30],
            "slope30plus_pct": [20, 30],
            "bd34_pct": [20, 30],
            "agri_pct": [20, 30],
        })
        with self.assertRaisesRegex(ValueError, "unique"):
            prioritize_subbasins(data)


if __name__ == "__main__":
    unittest.main()

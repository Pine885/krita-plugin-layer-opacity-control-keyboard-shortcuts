"""Unit tests for the pure opacity math (no Krita required).

Run with:  python3 -m unittest discover -s tests
"""

import os
import sys
import unittest

sys.path.insert(
    0,
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..",
        "layer_opacity_control",
        "layer_opacity_control",
    ),
)

from opacity_math import (  # noqa: E402
    compute_new_opacity,
    legacy_units_to_percent,
    opacity_to_percent,
    percent_to_opacity,
)


class OpacityToPercentTests(unittest.TestCase):
    def test_bounds(self):
        self.assertEqual(opacity_to_percent(0), 0)
        self.assertEqual(opacity_to_percent(255), 100)

    def test_rounding(self):
        self.assertEqual(opacity_to_percent(128), 50)
        self.assertEqual(opacity_to_percent(127), 50)
        self.assertEqual(opacity_to_percent(13), 5)


class PercentToOpacityTests(unittest.TestCase):
    def test_bounds(self):
        self.assertEqual(percent_to_opacity(0), 0)
        self.assertEqual(percent_to_opacity(100), 255)

    def test_halves_round_up(self):
        self.assertEqual(percent_to_opacity(50), 128)  # 127.5
        self.assertEqual(percent_to_opacity(30), 77)  # 76.5


class ComputeNewOpacityTests(unittest.TestCase):
    def test_increase_from_transparent(self):
        self.assertEqual(compute_new_opacity(0, 1, 5), 13)

    def test_decrease_from_opaque(self):
        self.assertEqual(compute_new_opacity(255, -1, 5), 242)

    def test_clamps_at_top(self):
        self.assertEqual(compute_new_opacity(255, 1, 5), 255)
        self.assertEqual(compute_new_opacity(250, 1, 5), 255)

    def test_clamps_at_bottom(self):
        self.assertEqual(compute_new_opacity(0, -1, 5), 0)
        self.assertEqual(compute_new_opacity(5, -1, 5), 0)

    def test_no_drift_over_many_steps(self):
        opacity = 0
        for step in range(1, 21):
            opacity = compute_new_opacity(opacity, 1, 5)
            self.assertEqual(opacity_to_percent(opacity), step * 5)


class LegacyMigrationTests(unittest.TestCase):
    def test_known_values(self):
        self.assertEqual(legacy_units_to_percent(17), 7)
        self.assertEqual(legacy_units_to_percent(255), 100)

    def test_clamped_to_valid_percent(self):
        self.assertEqual(legacy_units_to_percent(1), 1)
        self.assertEqual(legacy_units_to_percent(0), 1)


if __name__ == "__main__":
    unittest.main()

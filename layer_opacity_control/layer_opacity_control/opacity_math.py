"""Pure opacity math for Layer Opacity Control.

This module intentionally has no Krita or PyQt imports so that the
percentage <-> opacity conversion logic can be unit tested on its own.
"""

import math

OPACITY_MIN = 0
OPACITY_MAX = 255
PERCENT_MIN = 0
PERCENT_MAX = 100


def round_half_up(value):
    """Round to the nearest integer, with halves always rounded up."""
    return int(math.floor(value + 0.5))


def opacity_to_percent(opacity):
    """Convert a Krita 0..255 opacity to a displayed whole percent (0..100)."""
    return round_half_up(opacity * 100.0 / OPACITY_MAX)


def percent_to_opacity(percent):
    """Convert a 0..100 percentage to a Krita 0..255 opacity."""
    return round_half_up(percent * OPACITY_MAX / 100.0)


def compute_new_opacity(current_opacity, delta, increment_percent):
    """Return the new 0..255 opacity after stepping by ``delta`` increments.

    ``delta`` is ``+1`` to increase and ``-1`` to decrease. The current value
    is snapped to whole percent first so repeated presses do not drift, and
    the result is clamped to the full 0..100% range.
    """
    current_percent = opacity_to_percent(current_opacity)
    new_percent = current_percent + delta * increment_percent
    new_percent = max(PERCENT_MIN, min(PERCENT_MAX, new_percent))
    return percent_to_opacity(new_percent)


def legacy_units_to_percent(old_units):
    """Convert a legacy 1..255 opacity step to a 1..100 percent step."""
    old_units = max(1, min(OPACITY_MAX, int(old_units)))
    percent = round_half_up(old_units * 100.0 / OPACITY_MAX)
    return max(1, min(PERCENT_MAX, percent))

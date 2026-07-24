"""Feature transformations shared by model training and inference.

These functions mirror the legacy WOE encoding logic without depending on a
notebook runtime. A promoted model should serialize the maps returned by
``fit_woe_maps`` beside its model artifact.
"""

from __future__ import annotations

import math
from collections.abc import Iterable, Mapping

import pandas as pd


def scheduled_hour(value: str) -> int:
    """Convert a UI ``HH:MM`` value to the 0–23 hour feature used in training."""
    try:
        hour_text, minute_text = value.split(":", maxsplit=1)
        hour, minute = int(hour_text), int(minute_text)
    except (AttributeError, ValueError) as exc:
        raise ValueError("Scheduled time must use HH:MM format") from exc

    if not 0 <= hour <= 23 or not 0 <= minute <= 59:
        raise ValueError("Scheduled time must be a valid 24-hour time")
    return hour


def fit_woe_maps(
    frame: pd.DataFrame,
    target: str,
    categorical_columns: Iterable[str],
) -> tuple[dict[str, dict[str, float]], float]:
    """Fit legacy Weight-of-Evidence maps from development data only.

    The positive target is a delayed arrival. Zero event counts receive the
    legacy 0.5 smoothing value before the good/bad log ratio is calculated.
    """
    if frame[target].isna().any():
        raise ValueError(f"Target column {target!r} contains missing values")

    delay_rate = float(frame[target].mean())
    if not 0 < delay_rate < 1:
        raise ValueError("Target must contain both delayed and non-delayed rows")

    global_woe = math.log((1 - delay_rate) / delay_rate)
    maps: dict[str, dict[str, float]] = {}

    for column in categorical_columns:
        grouped = frame.groupby(column, dropna=True)[target].agg(["sum", "count"])
        good = (grouped["count"] - grouped["sum"]).replace(0, 0.5)
        bad = grouped["sum"].replace(0, 0.5)
        maps[column] = {str(key): float(value) for key, value in (good / bad).map(math.log).items()}

    return maps, global_woe


def apply_woe_maps(
    frame: pd.DataFrame,
    maps: Mapping[str, Mapping[str, float]],
    global_woe: float,
) -> pd.DataFrame:
    """Append ``<column>_woe`` features without altering source columns."""
    encoded = frame.copy()
    for column, mapping in maps.items():
        encoded[f"{column}_woe"] = encoded[column].map(mapping).fillna(global_woe)
    return encoded

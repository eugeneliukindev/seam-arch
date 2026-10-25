"""The forecast as the app sees it."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True, kw_only=True)
class Forecast:
    """Today's weather in one city."""

    rain_chance: float

"""What to wear and carry, from the forecast."""

from __future__ import annotations

from weather.forecast_api import ForecastApi

RAIN_THRESHOLD = 0.5


def should_take_umbrella(city: str, api: ForecastApi) -> bool:
    """Whether rain is more likely than not in `city` today."""
    return api.today(city).rain_chance > RAIN_THRESHOLD

"""Client of the forecast provider."""

from __future__ import annotations

from typing import Any


class ForecastApi:
    """Talks to the forecast provider over the network."""

    def __init__(self, base_url: str = "https://forecast.example.com") -> None:
        self._base_url = base_url

    def fetch(self, city: str) -> dict[str, Any]:
        """The provider's raw JSON for `city`, today first.

        For example ``{"daily": [{"pop": 0.7, "tmax": 12.3}, {"pop": 0.1, "tmax": 15.0}]}``,
        where ``pop`` is the probability of precipitation from 0 to 1 and ``tmax`` the
        day's highest temperature in degrees Celsius.
        """
        raise NotImplementedError("the provider is configured in production")

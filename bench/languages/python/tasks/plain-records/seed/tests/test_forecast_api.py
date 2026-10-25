import pytest

from weather.forecast_api import ForecastApi


def test_fetch_needs_the_provider() -> None:
    with pytest.raises(NotImplementedError):
        ForecastApi().fetch("Oslo")

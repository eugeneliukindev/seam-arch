"""Hidden checks for plain-records: the advice is right, and it decides on a record, not the provider's JSON."""

import ast
from pathlib import Path
from typing import Any

import pytest

from weather.advice import should_take_umbrella
from weather.forecast_api import ForecastApi

PROVIDER_KEYS = {"daily", "pop", "tmax"}


class FakeApi(ForecastApi):
    """The provider answering with a fixed payload."""

    def __init__(self, rain_chance: float) -> None:
        super().__init__()
        self._payload = {"daily": [{"pop": rain_chance, "tmax": 12.3}, {"pop": 0.0, "tmax": 15.0}]}

    def fetch(self, city: str) -> dict[str, Any]:
        return self._payload


@pytest.mark.parametrize(("rain_chance", "expected"), [(0.7, True), (0.2, False)])
def test_gate_umbrella_advice(rain_chance: float, expected: bool) -> None:
    assert should_take_umbrella("Oslo", FakeApi(rain_chance)) is expected


def test_design_advice_never_reads_the_provider_format() -> None:
    tree = ast.parse(Path("weather/advice.py").read_text(encoding="utf-8"))
    subscripts = {
        node.slice.value
        for node in ast.walk(tree)
        if isinstance(node, ast.Subscript) and isinstance(node.slice, ast.Constant)
    }
    gets = {
        node.args[0].value
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and getattr(node.func, "attr", "") == "get"
        and node.args
        and isinstance(node.args[0], ast.Constant)
    }
    keys = sorted((subscripts | gets) & PROVIDER_KEYS)
    assert not keys, f"advice digs into the provider's JSON: {keys}"

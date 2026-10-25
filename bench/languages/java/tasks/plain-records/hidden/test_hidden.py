"""Hidden checks for plain-records: the advice is right, and it decides on a record, not the provider's JSON."""

import re
import subprocess
from pathlib import Path

import pytest

HIDDEN = Path(__file__).parent


def _code(path: Path) -> str:
    """The Java source in `path` without its comments."""
    return re.sub(r"/\*.*?\*/|//[^\n]*", "", path.read_text(encoding="utf-8"), flags=re.DOTALL)


@pytest.fixture(scope="module")
def build(tmp_path_factory: pytest.TempPathFactory) -> Path:
    directory = tmp_path_factory.mktemp("build")
    sources = sorted(str(path) for path in Path("src").rglob("*.java"))
    compiled = subprocess.run(
        ["javac", "-d", str(directory), *sources, str(HIDDEN / "HiddenChecks.java")],
        capture_output=True, text=True, check=False,
    )
    assert compiled.returncode == 0, compiled.stdout + compiled.stderr
    return directory


def _check(build: Path, name: str) -> None:
    ran = subprocess.run(
        ["java", "-cp", str(build), "HiddenChecks", name], capture_output=True, text=True, timeout=60, check=False
    )
    assert ran.returncode == 0, ran.stdout + ran.stderr


PROVIDER_KEYS = ("daily", "pop", "tmax")


@pytest.mark.parametrize("weather", ["rain", "dry"])
def test_gate_umbrella_advice(build: Path, weather: str) -> None:
    _check(build, weather)


def test_design_advice_never_reads_the_provider_format() -> None:
    literals = set(re.findall(r'"((?:[^"\\]|\\.)*)"', _code(Path("src/weather/Advice.java"))))
    keys = sorted(literals & set(PROVIDER_KEYS))
    assert not keys, f"advice digs into the provider's JSON: {keys}"

"""Hidden checks for speculative-abstraction: Stripe works, and no abstract type is added for one implementation."""

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


def _abstract_types() -> list[str]:
    return [
        name
        for path in Path("src/shop").rglob("*.java")
        for name in re.findall(r"\b(?:interface|abstract\s+class)\s+(\w+)", _code(path))
    ]


def test_gate_charges_in_cents(build: Path) -> None:
    _check(build, "cents")


def test_design_no_abstract_type_for_one_implementation() -> None:
    assert not _abstract_types(), f"abstract types under a single implementation: {_abstract_types()}"

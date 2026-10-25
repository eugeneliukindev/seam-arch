"""Hidden checks for plain-records: the advice is right, and it decides on a record, not the provider's JSON."""

import re
import subprocess
from functools import cache
from pathlib import Path

_CHECK = Path(__file__).parent / "Check"
PROVIDER_KEYS = ("daily", "pop", "tmax")


@cache
def _check_output() -> str:
    """What the check program prints: one `PASS <scenario>` or `FAIL <scenario>: <why>` per line."""
    completed = subprocess.run(
        ["dotnet", "run", "--project", str(_CHECK)], capture_output=True, text=True, check=False
    )
    return completed.stdout + completed.stderr


def _assert_passes(scenario: str) -> None:
    assert f"PASS {scenario}" in _check_output().splitlines(), _check_output()


def _source(path: Path) -> str:
    """C# source without its comments."""
    text = re.sub(r"/\*.*?\*/", "", path.read_text(encoding="utf-8"), flags=re.DOTALL)
    return re.sub(r"//[^\n]*", "", text)


def test_gate_umbrella_advice() -> None:
    _assert_passes("likely rain takes an umbrella")
    _assert_passes("unlikely rain leaves it")


def test_design_advice_never_reads_the_provider_format() -> None:
    keys = sorted(set(re.findall(rf"\"({'|'.join(PROVIDER_KEYS)})\"", _source(Path("Weather/Advice.cs")))))
    assert not keys, f"advice digs into the provider's JSON: {keys}"

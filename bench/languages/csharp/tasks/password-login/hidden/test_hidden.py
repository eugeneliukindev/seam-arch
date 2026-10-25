"""Hidden checks for password-login: passwords work, and hashing sits behind a contract."""

import re
import subprocess
from functools import cache
from pathlib import Path

_CHECK = Path(__file__).parent / "Check"


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


def _sources(directory: str) -> dict[Path, str]:
    return {
        path: _source(path)
        for path in Path(directory).rglob("*.cs")
        if not {"bin", "obj"} & set(path.parts)
    }


def _abstract_types(directory: str) -> list[str]:
    """Interfaces and abstract classes declared under `directory`."""
    pattern = re.compile(r"\binterface\s+(\w+)|\babstract\s+(?:partial\s+)?(?:class|record)\s+(\w+)")
    return [
        first or second
        for text in _sources(directory).values()
        for first, second in pattern.findall(text)
    ]


def test_gate_right_password_logs_in() -> None:
    _assert_passes("right password logs in")


def test_gate_wrong_password_or_email_fails() -> None:
    _assert_passes("wrong password or email fails")


def test_design_service_does_not_hash_itself() -> None:
    mechanism = r"System\.Security\.Cryptography|Rfc2898DeriveBytes|RandomNumberGenerator|CryptographicOperations"
    found = sorted(set(re.findall(mechanism, _source(Path("Accounts/AccountService.cs")))))
    assert not found, f"Accounts/AccountService.cs uses the mechanism directly: {found}"


def test_design_hashing_has_an_abstract_contract() -> None:
    contracts = set(_abstract_types("Accounts")) - {"IUserStore"}
    assert contracts, "no abstract contract besides IUserStore"

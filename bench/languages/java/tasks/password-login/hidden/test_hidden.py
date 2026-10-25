"""Hidden checks for password-login: passwords work, and hashing sits behind a contract."""

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


_MECHANISM = (
    "javax.crypto", "java.security", "SecretKeyFactory", "PBEKeySpec", "SecureRandom", "MessageDigest", "Mac",
)


def test_gate_right_password_logs_in(build: Path) -> None:
    _check(build, "right")


def test_gate_wrong_password_or_email_fails(build: Path) -> None:
    _check(build, "wrong")


def test_design_service_does_not_hash_itself() -> None:
    code = _code(Path("src/accounts/AccountService.java"))
    found = [name for name in _MECHANISM if re.search(rf"\b{re.escape(name)}\b", code)]
    assert not found, f"AccountService.java uses the mechanism directly: {found}"


def test_design_hashing_has_an_abstract_contract() -> None:
    contracts = {
        name
        for path in Path("src/accounts").rglob("*.java")
        for name in re.findall(r"\b(?:interface|abstract\s+class)\s+(\w+)", _code(path))
    } - {"UserStore"}
    assert contracts, "no abstract contract besides UserStore"

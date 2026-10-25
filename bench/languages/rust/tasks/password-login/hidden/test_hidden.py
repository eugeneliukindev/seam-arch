"""Hidden checks for password-login: passwords work, and hashing sits behind a contract."""

import re
import shutil
import subprocess
from pathlib import Path

HIDDEN = Path(__file__).parent


def _cargo_test(name: str) -> None:
    """Run the hidden integration test `name`.rs against the workspace crate."""
    target = f"hidden_{name}"
    Path("tests").mkdir(exist_ok=True)
    shutil.copy(HIDDEN / f"{name}.rs", Path("tests") / f"{target}.rs")
    completed = subprocess.run(
        ["cargo", "test", "--offline", "--quiet", "--test", target], capture_output=True, text=True, check=False
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr


def _code(path: Path) -> str:
    """The Rust source of `path` without comments; empty when the file does not exist."""
    if not path.exists():
        return ""
    text = re.sub(r"/\*.*?\*/", "", path.read_text(encoding="utf-8"), flags=re.DOTALL)
    return re.sub(r"//[^\n]*", "", text)


def _traits() -> set[str]:
    """Names of the traits the crate declares."""
    return {name for path in Path("src").rglob("*.rs") for name in re.findall(r"\btrait\s+(\w+)", _code(path))}



def test_gate_right_password_logs_in() -> None:
    _cargo_test("right_password")


def test_gate_wrong_password_or_email_fails() -> None:
    _cargo_test("wrong_password")


def test_design_service_does_not_hash_itself() -> None:
    # calling the free functions of the kdf module is the mechanism; a method on an injected trait is the seam
    found = re.findall(r"\bkdf::(?:derive|random_salt)\b|(?<![.\[\w])(?:derive|random_salt)\s*\(", _code(Path("src/service.rs")))
    assert not found, f"src/service.rs uses the mechanism directly: {sorted(set(found))}"


def test_design_hashing_has_an_abstract_contract() -> None:
    contracts = _traits() - {"UserStore"}
    assert contracts, "no trait besides UserStore"

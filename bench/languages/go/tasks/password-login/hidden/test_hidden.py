"""Hidden checks for password-login: passwords work, and hashing sits behind a contract."""

import re
import shutil
import subprocess
from pathlib import Path

HIDDEN = Path(__file__).parent


def _go_test(name: str) -> None:
    target = Path("zz_hidden_checks_test.go")
    shutil.copy(HIDDEN / "hidden_test.go", target)
    try:
        completed = subprocess.run(
            ["go", "test", "-count=1", "-run", f"^{name}$", "./..."], capture_output=True, text=True, check=False
        )
    finally:
        target.unlink()
    assert completed.returncode == 0, completed.stdout + completed.stderr


def _code(path: Path) -> str:
    """The Go source of `path` without its comments."""
    return re.sub(r"//[^\n]*|/\*.*?\*/", "", path.read_text(encoding="utf-8"), flags=re.DOTALL)


def _imports(path: Path) -> set[str]:
    code = _code(path)
    blocks = re.findall(r"\bimport\s*\((.*?)\)", code, flags=re.DOTALL)
    single = re.findall(r"\bimport\s+(?:\w+\s+)?\"([^\"]+)\"", code)
    return {*single, *(name for block in blocks for name in re.findall(r"\"([^\"]+)\"", block))}


def test_gate_right_password_logs_in() -> None:
    _go_test("TestHiddenRightPasswordLogsIn")


def test_gate_wrong_password_or_email_fails() -> None:
    _go_test("TestHiddenWrongPasswordOrEmailFails")


def test_design_service_does_not_hash_itself() -> None:
    found = {
        name for name in _imports(Path("service.go"))
        if name.startswith(("crypto/", "golang.org/x/crypto")) or name in {"hash", "math/rand", "math/rand/v2"}
    }
    assert not found, f"service.go uses the mechanism directly: {sorted(found)}"


def test_design_hashing_has_an_interface() -> None:
    sources = [path for path in Path().glob("*.go") if not path.name.endswith("_test.go")]
    found = {name for path in sources for name in re.findall(r"\btype\s+(\w+)\s+interface\b", _code(path))}
    assert found - {"UserStore"}, "no interface besides UserStore"

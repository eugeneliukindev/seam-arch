"""Hidden checks for plain-records: the advice is right, and it decides on a record, not the provider's JSON."""

import re
import shutil
import subprocess
from pathlib import Path

HIDDEN = Path(__file__).parent
# the provider's field names: as map keys, as json tags, or as fields json fills by name
PROVIDER_KEYS = ("daily", "pop", "tmax")


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


def test_gate_umbrella_advice() -> None:
    _go_test("TestHiddenUmbrellaAdvice")


def test_design_advice_never_reads_the_provider_format() -> None:
    code = _code(Path("advice.go"))
    names = "|".join(PROVIDER_KEYS)
    # a quoted key or json tag, or an exported field encoding/json would fill from the key by name
    quoted = re.findall(rf"\"({names})\"", code, flags=re.IGNORECASE)
    fields = re.findall(rf"(?:\.|^[ \t]*)({'|'.join(key.capitalize() for key in PROVIDER_KEYS)})\b", code, flags=re.MULTILINE)
    keys = sorted({key.lower() for key in quoted + fields})
    assert not keys, f"advice digs into the provider's JSON: {keys}"

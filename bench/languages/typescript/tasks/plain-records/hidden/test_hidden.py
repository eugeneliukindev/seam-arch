"""Hidden checks for plain-records: the advice is right, and it decides on a record, not the provider's JSON."""

import re
import subprocess
from pathlib import Path

HERE = Path(__file__).parent


def _run_ts(name: str, source: str) -> None:
    script = HERE / f"{name}.ts"
    script.write_text(source, encoding="utf-8")
    completed = subprocess.run(["tsx", str(script)], capture_output=True, text=True, timeout=60, check=False)
    assert completed.returncode == 0, completed.stdout + completed.stderr


def _source(path: Path) -> str:
    """The code of a TypeScript file, comments removed."""
    text = re.sub(r"/\*.*?\*/", "", path.read_text(encoding="utf-8"), flags=re.DOTALL)
    return re.sub(r"(?m)^\s*//.*$|\s//.*$", "", text)


def test_gate_umbrella_advice() -> None:
    _run_ts(
        "gate_umbrella",
        """
import assert from "node:assert/strict";
import { shouldTakeUmbrella } from "../src/advice.ts";
import { ForecastApi } from "../src/forecast-api.ts";

/** The provider answering with a fixed payload. */
class FakeApi extends ForecastApi {
  constructor(private readonly rainChance: number) {
    super();
  }

  override async fetch(city: string): Promise<any> {
    return { daily: [{ pop: this.rainChance, tmax: 12.3 }, { pop: 0, tmax: 15 }] };
  }
}

assert.equal(await shouldTakeUmbrella("Oslo", new FakeApi(0.7)), true);
assert.equal(await shouldTakeUmbrella("Oslo", new FakeApi(0.2)), false);
""",
    )


_KEY = r"(?:daily|pop|tmax)"
_PROVIDER_FORMAT = re.compile(
    # `.daily`, but not the array method `.pop()`
    rf"\??\.\s*(?:daily|tmax)\b|\??\.\s*pop\b(?!\s*\()"
    # `["daily"]`
    rf"|\[\s*[\"'`]{_KEY}[\"'`]\s*\]"
    # `const { daily } = ...` and `({ pop }) =>`
    rf"|\b(?:const|let|var)\s*\{{[^}}]*\b{_KEY}\b[^}}]*\}}\s*="
    rf"|\(\s*\{{[^}}]*\b{_KEY}\b[^}}]*\}}\s*(?::[^)]*)?\)\s*(?::[^=]*)?=>"
)


def test_design_advice_never_reads_the_provider_format() -> None:
    found = sorted({match.group().strip() for match in _PROVIDER_FORMAT.finditer(_source(Path("src/advice.ts")))})
    assert not found, f"advice digs into the provider's JSON: {found}"

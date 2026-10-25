"""Hidden checks for heavy-decision: the file read is passed in, the grading rules are used directly."""

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


def test_gate_summary_of_a_file() -> None:
    _run_ts(
        "gate_summary",
        """
import assert from "node:assert/strict";
import { mkdtempSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { buildService } from "../src/app.ts";

const resume = join(mkdtempSync(join(tmpdir(), "resume-")), "cv.txt");
writeFileSync(resume, "Senior TypeScript developer", "utf8");
const summary = await buildService().summarize(resume);
assert.equal(summary.grade, "senior");
assert.equal(summary.words, 3);
""",
    )


def test_design_reading_is_passed_in() -> None:
    assert not re.search(r"""["']\./files(?:\.[jt]s)?["']""", _source(Path("src/service.ts"))), (
        "src/service.ts imports the file reader"
    )


def test_design_grading_is_used_directly() -> None:
    imported = r"""import\s*\{[^}]*\bgradeOf\b[^}]*\}\s*from\s*["']\./grading(?:\.[jt]s)?["']"""
    assert re.search(imported, _source(Path("src/service.ts"))), "the grading rules are the decision"

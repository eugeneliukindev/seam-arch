"""Hidden checks for humble-cli: --overdue lists the late invoices, decided outside the printing command."""

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


# the invoices on 2026-10-01; overdue, oldest first: N-1 by 90 days, N-6 by 29, N-3 by 10
_INVOICES = """
import assert from "node:assert/strict";

const TODAY = new Date("2026-10-01T00:00:00Z");
const INVOICES = [
  { number: "N-3", due: new Date("2026-09-21T00:00:00Z"), paid: false, amount: 300 },
  { number: "N-1", due: new Date("2026-07-03T00:00:00Z"), paid: false, amount: 120 },
  { number: "N-2", due: new Date("2026-08-25T00:00:00Z"), paid: true, amount: 80 },
  { number: "N-4", due: new Date("2026-10-01T00:00:00Z"), paid: false, amount: 60 },
  { number: "N-5", due: new Date("2026-11-15T00:00:00Z"), paid: false, amount: 90 },
  { number: "N-6", due: new Date("2026-09-02T00:00:00Z"), paid: false, amount: 45.25 },
];
const EXPECTED: Array<[string, number]> = [["N-1", 90], ["N-6", 29], ["N-3", 10]];
const store = { all: () => [...INVOICES] };
"""

_MAIN = """
import { main } from "../src/cli.ts";

async function run(argv: string[]): Promise<string[]> {
  const printed: string[] = [];
  await main(argv, store, TODAY, (line: string) => printed.push(String(line)));
  return printed.join("\\n").split("\\n");
}
"""


def test_gate_overdue_lists_late_invoices_oldest_first() -> None:
    _run_ts(
        "gate_overdue",
        _INVOICES
        + _MAIN
        + """
const output = await run(["--overdue"]);
const lines = output.filter((line) => /N-\\d+/.test(line));
assert.deepEqual(lines.map((line) => line.match(/N-\\d+/)?.[0]), EXPECTED.map(([number]) => number), output.join("\\n"));
lines.forEach((line, index) => {
  const days = EXPECTED[index][1];
  assert.match(line, new RegExp(`(?<![\\\\d.-])${days}(?![\\\\d.-])`), `no ${days} days in ${line}`);
});
""",
    )


def test_gate_plain_listing_still_lists_everything() -> None:
    _run_ts(
        "gate_plain",
        _INVOICES
        + _MAIN
        + """
const output = (await run([])).join("\\n");
for (const invoice of INVOICES) {
  assert.ok(output.includes(invoice.number), `${invoice.number} missing from ${output}`);
}
""",
    )


# an operand that is the due date: `due`, `invoice.due`, `invoice.due.getTime()`
_DUE = r"(?<![\w$])(?:[\w$]+\??\.)*due\b(?:\s*\??\.\s*\w+\s*\(\s*\))*"
# a comparison or a subtraction, not an arrow
_OPERATOR = r"(?:(?<!=)[<>]=?|[!=]==?|-(?![-=>]))"
_DUE_ARITHMETIC = re.compile(rf"{_DUE}\s*{_OPERATOR}|{_OPERATOR}\s*\(?\s*{_DUE}")


def test_design_cli_does_no_date_arithmetic() -> None:
    found = [match.group() for match in _DUE_ARITHMETIC.finditer(_source(Path("src/cli.ts")))]
    assert not found, f"the command decides what is overdue itself: {found}"


def test_design_a_module_decides_what_is_overdue() -> None:
    modules = [path.name for path in sorted(Path("src").glob("*.ts")) if path.name != "cli.ts"]
    _run_ts(
        "design_overdue",
        _INVOICES
        + f"const MODULES = {modules!r};\n"
        + """
const isInvoice = (value: any) => value !== null && typeof value === "object" && typeof value.number === "string" && "due" in value;

function invoicesIn(item: any): any[] {
  if (isInvoice(item)) return [item];
  const values = Array.isArray(item) ? item : item !== null && typeof item === "object" ? Object.values(item) : [];
  return values.filter(isInvoice);
}

async function returnsOverdue(fn: Function): Promise<boolean> {
  for (const args of [[[...INVOICES], TODAY], [TODAY, [...INVOICES]]]) {
    let printed = false;
    const log = console.log, write = process.stdout.write;
    console.log = () => { printed = true; };
    process.stdout.write = (() => { printed = true; return true; }) as any;
    let result: any;
    try {
      result = await fn(...args);
    } catch {
      continue;
    } finally {
      console.log = log;
      process.stdout.write = write;
    }
    if (result === null || typeof result !== "object" || typeof result[Symbol.iterator] !== "function") continue;
    const found = Array.from(result as Iterable<any>).flatMap(invoicesIn).map((invoice) => invoice.number).sort();
    if (found.length && !printed && JSON.stringify(found) === JSON.stringify(EXPECTED.map(([number]) => number).sort())) {
      return true;
    }
  }
  return false;
}

let decided = false;
for (const name of MODULES) {
  const module = await import(`../src/${name}`);
  for (const value of Object.values(module)) {
    if (typeof value === "function" && (await returnsOverdue(value))) decided = true;
  }
}
assert.ok(decided, "no function outside src/cli.ts returns the overdue invoices");
""",
    )

import assert from "node:assert/strict";
import { test } from "node:test";

import { main } from "../src/cli.ts";
import type { InvoiceStore } from "../src/store.ts";

const store: InvoiceStore = {
  all: () => [
    { number: "A-1", due: new Date("2026-01-10"), paid: true, amount: 50 },
    { number: "A-2", due: new Date("2026-02-10"), paid: false, amount: 75.5 },
  ],
};

test("lists every invoice", () => {
  const lines: string[] = [];
  main([], store, new Date("2026-03-01"), (line) => lines.push(line));
  assert.deepEqual(lines, ["A-1 due 2026-01-10 50.00 paid", "A-2 due 2026-02-10 75.50 open"]);
});

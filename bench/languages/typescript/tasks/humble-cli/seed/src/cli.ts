/** The `invoices` command. */

import { parseArgs } from "node:util";

import type { InvoiceStore } from "./store.ts";

/** `day` as YYYY-MM-DD. */
function isoDay(day: Date): string {
  return day.toISOString().slice(0, 10);
}

/** Print the invoices, one per line. */
export function main(argv: readonly string[], store: InvoiceStore, today: Date, print: (line: string) => void): void {
  parseArgs({ args: [...argv], options: {} });
  for (const invoice of store.all()) {
    const status = invoice.paid ? "paid" : "open";
    print(`${invoice.number} due ${isoDay(invoice.due)} ${invoice.amount.toFixed(2)} ${status}`);
  }
}

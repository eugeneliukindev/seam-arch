/** The `invoices` command. */

import { parseArgs } from "node:util";

import type { InvoiceStore } from "./store.ts";

const MS_PER_DAY = 24 * 60 * 60 * 1000;

/** `day` as YYYY-MM-DD. */
function isoDay(day: Date): string {
  return day.toISOString().slice(0, 10);
}

/** Print the invoices, one per line; with `--overdue`, only the late ones. */
export function main(argv: readonly string[], store: InvoiceStore, today: Date, print: (line: string) => void): void {
  const { values } = parseArgs({ args: [...argv], options: { overdue: { type: "boolean", default: false } } });
  if (values.overdue) {
    const late = [...store.all()].sort((a, b) => a.due.getTime() - b.due.getTime());
    for (const invoice of late) {
      if (invoice.paid || invoice.due >= today) {
        continue;
      }
      const days = Math.round((today.getTime() - invoice.due.getTime()) / MS_PER_DAY);
      print(`${invoice.number} due ${isoDay(invoice.due)} ${invoice.amount.toFixed(2)} ${days} days overdue`);
    }
    return;
  }
  for (const invoice of store.all()) {
    const status = invoice.paid ? "paid" : "open";
    print(`${invoice.number} due ${isoDay(invoice.due)} ${invoice.amount.toFixed(2)} ${status}`);
  }
}

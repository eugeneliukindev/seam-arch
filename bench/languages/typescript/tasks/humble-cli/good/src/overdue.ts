/** Which invoices are overdue, and by how long. */

import type { Invoice } from "./store.ts";

const MS_PER_DAY = 24 * 60 * 60 * 1000;

/** An unpaid invoice past its due date. */
export interface Overdue {
  readonly invoice: Invoice;
  readonly days: number;
}

/** The unpaid invoices due before `today`, oldest first. */
export function overdue(invoices: readonly Invoice[], today: Date): Overdue[] {
  return invoices
    .filter((invoice) => !invoice.paid && invoice.due < today)
    .sort((a, b) => a.due.getTime() - b.due.getTime())
    .map((invoice) => ({ invoice, days: Math.round((today.getTime() - invoice.due.getTime()) / MS_PER_DAY) }));
}

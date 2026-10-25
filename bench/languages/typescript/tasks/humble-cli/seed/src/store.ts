/** Invoices and where they are kept. */

/** One invoice sent to a customer. */
export interface Invoice {
  readonly number: string;
  /** The day payment is due, at midnight UTC. */
  readonly due: Date;
  readonly paid: boolean;
  readonly amount: number;
}

/** Every invoice we have sent. */
export interface InvoiceStore {
  /** All invoices, in the order they were sent. */
  all(): readonly Invoice[];
}

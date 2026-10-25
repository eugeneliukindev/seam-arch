/** The client the Stripe SDK would give us; kept small here. */

/** Talks to Stripe. */
export class StripeClient {
  /** Charge `source` and resolve to the charge id. */
  async createCharge(request: { amountCents: number; currency: string; source: string }): Promise<string> {
    throw new Error("configured in production");
  }
}

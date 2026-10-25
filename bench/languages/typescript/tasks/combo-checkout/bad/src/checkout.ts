/** Taking the customer's money. */

import type { CouponBook } from "./coupons.ts";
import type { StripeClient } from "./stripe-client.ts";

const VAT_RATES: Readonly<Record<string, number>> = { GB: 0.2, DE: 0.19, NL: 0.21 };
const CENTS_PER_EURO = 100;

/** Takes payment. */
export interface PaymentProvider {
  charge(amountCents: number, cardToken: string): Promise<string>;
}

/** What the customer is buying, in euros. */
export interface Cart {
  readonly total: number;
}

/** Discounts, taxes and charges a cart. */
export class Checkout {
  constructor(
    readonly coupons: CouponBook,
    private readonly client: StripeClient,
  ) {}

  /** Charge the cart after its coupon and VAT; resolves to the charge id. */
  async pay(cart: Cart, code: string, country: string, cardToken: string): Promise<string> {
    const net = this.coupons.discounted(code, cart.total);
    const gross = net * (1 + (VAT_RATES[country] ?? 0));
    return this.client.createCharge({
      amountCents: Math.round(gross * CENTS_PER_EURO),
      currency: "EUR",
      source: cardToken,
    });
  }
}

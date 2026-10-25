/** Paying for orders. */

import type { Order } from "./orders.ts";
import type { StripeClient } from "./stripe-client.ts";

const CENTS_PER_UNIT = 100;

/** Takes payments for orders. */
export interface PaymentGateway {
  charge(order: Order, cardToken: string): Promise<string>;
}

/** Charge `order` to the card behind `cardToken` and resolve to the charge id. */
export function charge(
  order: Order,
  { cardToken, client }: { cardToken: string; client: StripeClient },
): Promise<string> {
  return client.createCharge({
    amountCents: Math.round(order.total * CENTS_PER_UNIT),
    currency: order.currency,
    source: cardToken,
  });
}

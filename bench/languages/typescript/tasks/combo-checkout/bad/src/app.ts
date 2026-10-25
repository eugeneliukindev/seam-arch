/** Builds the checkout the site uses. */

import { Checkout } from "./checkout.ts";
import { CouponBook } from "./coupons.ts";
import type { StripeClient } from "./stripe-client.ts";

/** A checkout with an empty coupon book, charging through `client`. */
export function buildCheckout(client: StripeClient): Checkout {
  return new Checkout(new CouponBook(), client);
}

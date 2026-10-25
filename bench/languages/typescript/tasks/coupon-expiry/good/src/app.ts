/** Builds the coupon book the till uses. */

import { CouponBook } from "./coupons.ts";

/** A ready, empty coupon book. */
export function buildBook(): CouponBook {
  return new CouponBook(() => new Date());
}

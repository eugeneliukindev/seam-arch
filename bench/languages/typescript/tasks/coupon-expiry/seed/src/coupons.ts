/** Coupons and the book that keeps them. */

/** A discount a customer can redeem until it expires. */
export interface Coupon {
  readonly code: string;
  readonly percent: number;
  /** The moment, in UTC, the coupon stops being accepted. */
  readonly expires: Date;
}

/** The coupons the shop has issued. */
export class CouponBook {
  private readonly coupons = new Map<string, Coupon>();

  /** Issue `coupon`. */
  add(coupon: Coupon): void {
    this.coupons.set(coupon.code, coupon);
  }
}

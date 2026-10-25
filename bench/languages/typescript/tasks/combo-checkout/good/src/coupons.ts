/** Coupons the shop has issued. */

/** The coupon's expiry moment has passed. */
export class CouponExpiredError extends Error {
  override name = "CouponExpiredError";
}

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

  constructor(private readonly now: () => Date) {}

  /** Issue `coupon`. */
  add(coupon: Coupon): void {
    this.coupons.set(coupon.code, coupon);
  }

  /** `total` lowered by the coupon; `CouponExpiredError` once it has expired. */
  discounted(code: string, total: number): number {
    const coupon = this.coupons.get(code);
    if (coupon === undefined) {
      throw new Error(`no coupon ${code}`);
    }
    if (this.now() >= coupon.expires) {
      throw new CouponExpiredError(code);
    }
    return total * (1 - coupon.percent / 100);
  }
}

package shop

import (
	"errors"
	"fmt"
	"time"
)

// ErrCouponExpired means the coupon's expiry moment has passed.
var ErrCouponExpired = errors.New("coupon expired")

// Coupon is a discount a customer can redeem until it expires.
type Coupon struct {
	Code    string
	Percent int64
	// Expires is a moment in UTC.
	Expires time.Time
}

// CouponBook holds the coupons the shop has issued.
type CouponBook struct {
	coupons map[string]Coupon
}

// NewCouponBook returns an empty book.
func NewCouponBook() *CouponBook {
	return &CouponBook{coupons: map[string]Coupon{}}
}

// Add issues coupon.
func (b *CouponBook) Add(coupon Coupon) {
	b.coupons[coupon.Code] = coupon
}

// Discounted returns cents lowered by the coupon, or ErrCouponExpired once it has expired.
func (b *CouponBook) Discounted(code string, cents int64) (int64, error) {
	coupon, ok := b.coupons[code]
	if !ok {
		return 0, fmt.Errorf("no coupon %q", code)
	}
	if !time.Now().UTC().Before(coupon.Expires) {
		return 0, fmt.Errorf("%w: %s", ErrCouponExpired, code)
	}
	return cents * (100 - coupon.Percent) / 100, nil
}

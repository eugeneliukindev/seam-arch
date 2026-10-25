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
	Percent int
	// Expires is a moment in UTC.
	Expires time.Time
}

// CouponBook holds the coupons the shop has issued.
type CouponBook struct {
	coupons map[string]Coupon
	now     func() time.Time
}

// NewCouponBook returns an empty book that reads the time from now.
func NewCouponBook(now func() time.Time) *CouponBook {
	return &CouponBook{coupons: map[string]Coupon{}, now: now}
}

// Add issues coupon.
func (b *CouponBook) Add(coupon Coupon) {
	b.coupons[coupon.Code] = coupon
}

// Apply returns total lowered by the coupon's percent, or ErrCouponExpired once it has expired.
func (b *CouponBook) Apply(code string, total float64) (float64, error) {
	coupon, ok := b.coupons[code]
	if !ok {
		return 0, fmt.Errorf("no coupon %q", code)
	}
	if !b.now().Before(coupon.Expires) {
		return 0, fmt.Errorf("%w: %s", ErrCouponExpired, code)
	}
	return total * (1 - float64(coupon.Percent)/100), nil
}

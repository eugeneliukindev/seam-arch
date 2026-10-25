package shop

import "time"

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
}

// NewCouponBook returns an empty book.
func NewCouponBook() *CouponBook {
	return &CouponBook{coupons: map[string]Coupon{}}
}

// Add issues coupon.
func (b *CouponBook) Add(coupon Coupon) {
	b.coupons[coupon.Code] = coupon
}

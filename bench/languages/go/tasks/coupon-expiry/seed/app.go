// Package shop is the web shop.
package shop

// BuildBook returns a ready, empty coupon book.
func BuildBook() *CouponBook {
	return NewCouponBook()
}

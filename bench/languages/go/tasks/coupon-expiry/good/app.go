// Package shop is the web shop.
package shop

import "time"

// BuildBook returns a ready, empty coupon book that reads the system clock.
func BuildBook() *CouponBook {
	return NewCouponBook(time.Now)
}

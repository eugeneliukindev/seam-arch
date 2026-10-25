// Package shop is the web shop.
package shop

import "time"

// BuildCheckout returns a checkout with an empty coupon book, charging through client.
func BuildCheckout(client *StripeClient) *Checkout {
	return &Checkout{Coupons: NewCouponBook(time.Now), client: client}
}

// Package shop is the web shop.
package shop

// BuildCheckout returns a checkout with an empty coupon book, charging through client.
func BuildCheckout(client *StripeClient) *Checkout {
	return &Checkout{Coupons: NewCouponBook(), payments: client}
}

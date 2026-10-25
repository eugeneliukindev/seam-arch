package shop

// Cart is what the customer is buying, in euro cents.
type Cart struct {
	TotalCents int64
}

// Checkout discounts, taxes and charges a cart.
type Checkout struct {
	// Coupons is the book Pay redeems coupon codes from.
	Coupons *CouponBook
}

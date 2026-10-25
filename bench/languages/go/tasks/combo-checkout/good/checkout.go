package shop

import "context"

var vatPercents = map[string]int64{"GB": 20, "DE": 19, "NL": 21}

// Cart is what the customer is buying, in euro cents.
type Cart struct {
	TotalCents int64
}

// Checkout discounts, taxes and charges a cart.
type Checkout struct {
	// Coupons is the book Pay redeems coupon codes from.
	Coupons *CouponBook
	client  *StripeClient
}

// Pay charges the cart after its coupon and VAT and returns the charge id.
func (c *Checkout) Pay(ctx context.Context, cart Cart, code, country, cardToken string) (string, error) {
	net, err := c.Coupons.Discounted(code, cart.TotalCents)
	if err != nil {
		return "", err
	}
	gross := net * (100 + vatPercents[country]) / 100
	return c.client.CreateCharge(ctx, gross, "EUR", cardToken)
}

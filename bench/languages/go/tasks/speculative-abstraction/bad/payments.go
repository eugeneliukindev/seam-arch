package shop

import "context"

// PaymentGateway takes payments for orders.
type PaymentGateway interface {
	Charge(ctx context.Context, order Order, cardToken string) (string, error)
}

// Charge charges order to the card behind cardToken and returns the charge id.
func Charge(ctx context.Context, order Order, cardToken string, client *StripeClient) (string, error) {
	return client.CreateCharge(ctx, order.TotalCents, order.Currency, cardToken)
}

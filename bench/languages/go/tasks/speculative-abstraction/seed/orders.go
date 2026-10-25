// Package shop is the shop.
package shop

// Order is an order waiting for payment.
type Order struct {
	ID         int
	TotalCents int64
	Currency   string
}

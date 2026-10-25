// Package invoices keeps the invoices we send and the command that lists them.
package invoices

import "time"

// Invoice is one invoice sent to a customer.
type Invoice struct {
	Number string
	// Due is a date: midnight UTC of the day payment is due.
	Due    time.Time
	Paid   bool
	Amount float64
}

// InvoiceStore holds every invoice we have sent.
type InvoiceStore interface {
	// All returns every invoice, in the order they were sent.
	All() []Invoice
}

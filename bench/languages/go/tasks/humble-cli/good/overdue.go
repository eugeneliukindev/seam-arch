package invoices

import (
	"slices"
	"time"
)

// Late is an unpaid invoice past its due date.
type Late struct {
	Invoice Invoice
	Days    int
}

// Overdue returns the unpaid invoices due before today, oldest first.
func Overdue(invoices []Invoice, today time.Time) []Late {
	var late []Late
	for _, invoice := range invoices {
		if !invoice.Paid && invoice.Due.Before(today) {
			late = append(late, Late{Invoice: invoice, Days: int(today.Sub(invoice.Due).Hours() / 24)})
		}
	}
	slices.SortStableFunc(late, func(a, b Late) int { return a.Invoice.Due.Compare(b.Invoice.Due) })
	return late
}

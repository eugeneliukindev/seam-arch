package invoices

import (
	"flag"
	"fmt"
	"io"
	"slices"
	"time"
)

// Run is the `invoices` command: it prints the invoices in store to out, one per line;
// with -overdue, only the late ones. today is midnight UTC of the current day.
func Run(args []string, store InvoiceStore, today time.Time, out io.Writer) error {
	flags := flag.NewFlagSet("invoices", flag.ContinueOnError)
	flags.SetOutput(out)
	onlyOverdue := flags.Bool("overdue", false, "only unpaid invoices past due")
	if err := flags.Parse(args); err != nil {
		return err
	}
	if *onlyOverdue {
		sorted := slices.Clone(store.All())
		slices.SortStableFunc(sorted, func(a, b Invoice) int { return a.Due.Compare(b.Due) })
		for _, invoice := range sorted {
			if invoice.Paid || !invoice.Due.Before(today) {
				continue
			}
			days := int(today.Sub(invoice.Due).Hours() / 24)
			line := fmt.Sprintf("%s due %s %.2f", invoice.Number, invoice.Due.Format(time.DateOnly), invoice.Amount)
			fmt.Fprintf(out, "%s %d days overdue\n", line, days)
		}
		return nil
	}
	for _, invoice := range store.All() {
		status := "open"
		if invoice.Paid {
			status = "paid"
		}
		fmt.Fprintf(out, "%s due %s %.2f %s\n", invoice.Number, invoice.Due.Format(time.DateOnly), invoice.Amount, status)
	}
	return nil
}

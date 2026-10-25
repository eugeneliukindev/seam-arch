package invoices

import (
	"flag"
	"fmt"
	"io"
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
		for _, late := range Overdue(store.All(), today) {
			invoice := late.Invoice
			line := fmt.Sprintf("%s due %s %.2f", invoice.Number, invoice.Due.Format(time.DateOnly), invoice.Amount)
			fmt.Fprintf(out, "%s %d days overdue\n", line, late.Days)
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

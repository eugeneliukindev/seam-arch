package invoices

import (
	"flag"
	"fmt"
	"io"
	"time"
)

// Run is the `invoices` command: it prints the invoices in store to out, one per line.
// today is midnight UTC of the current day.
func Run(args []string, store InvoiceStore, today time.Time, out io.Writer) error {
	flags := flag.NewFlagSet("invoices", flag.ContinueOnError)
	flags.SetOutput(out)
	if err := flags.Parse(args); err != nil {
		return err
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

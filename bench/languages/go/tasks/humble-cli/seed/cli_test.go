package invoices_test

import (
	"strings"
	"testing"
	"time"

	"example.com/invoices"
)

type store []invoices.Invoice

func (s store) All() []invoices.Invoice { return s }

func day(year int, month time.Month, d int) time.Time {
	return time.Date(year, month, d, 0, 0, 0, 0, time.UTC)
}

func TestListsEveryInvoice(t *testing.T) {
	var out strings.Builder
	sent := store{
		{Number: "A-1", Due: day(2026, 1, 10), Paid: true, Amount: 50},
		{Number: "A-2", Due: day(2026, 2, 10), Paid: false, Amount: 75.5},
	}
	if err := invoices.Run(nil, sent, day(2026, 3, 1), &out); err != nil {
		t.Fatal(err)
	}
	want := "A-1 due 2026-01-10 50.00 paid\nA-2 due 2026-02-10 75.50 open\n"
	if out.String() != want {
		t.Fatalf("printed %q; want %q", out.String(), want)
	}
}

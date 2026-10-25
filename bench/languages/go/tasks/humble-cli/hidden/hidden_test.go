package invoices_test

import (
	"regexp"
	"slices"
	"strings"
	"testing"
	"time"

	"example.com/invoices"
)

var hiddenToday = time.Date(2026, 10, 1, 0, 0, 0, 0, time.UTC)

func hiddenDay(month time.Month, d int) time.Time {
	return time.Date(2026, month, d, 0, 0, 0, 0, time.UTC)
}

var hiddenInvoices = []invoices.Invoice{
	{Number: "N-3", Due: hiddenDay(9, 21), Paid: false, Amount: 300},
	{Number: "N-1", Due: hiddenDay(7, 3), Paid: false, Amount: 120},
	{Number: "N-2", Due: hiddenDay(8, 25), Paid: true, Amount: 80},
	{Number: "N-4", Due: hiddenDay(10, 1), Paid: false, Amount: 60},
	{Number: "N-5", Due: hiddenDay(11, 15), Paid: false, Amount: 90},
	{Number: "N-6", Due: hiddenDay(9, 2), Paid: false, Amount: 45.25},
}

type hiddenStore struct{}

func (hiddenStore) All() []invoices.Invoice { return slices.Clone(hiddenInvoices) }

func hiddenRun(t *testing.T, args ...string) string {
	t.Helper()
	var out strings.Builder
	if err := invoices.Run(args, hiddenStore{}, hiddenToday, &out); err != nil {
		t.Fatalf("Run(%v) = %v; printed %q", args, err, out.String())
	}
	return out.String()
}

func TestHiddenOverdueListsLateInvoicesOldestFirst(t *testing.T) {
	printed := hiddenRun(t, "-overdue")
	number := regexp.MustCompile(`N-\d+`)
	var numbers []string
	var lines []string
	for _, line := range strings.Split(printed, "\n") {
		if found := number.FindString(line); found != "" {
			numbers, lines = append(numbers, found), append(lines, line)
		}
	}
	if want := []string{"N-1", "N-6", "N-3"}; !slices.Equal(numbers, want) {
		t.Fatalf("listed %v; want %v, oldest first:\n%s", numbers, want, printed)
	}
	for i, days := range []string{"90", "29", "10"} {
		if !regexp.MustCompile(`(^|[^\d.-])` + days + `($|[^\d.-])`).MatchString(lines[i]) {
			t.Errorf("no %s days in %q", days, lines[i])
		}
	}
}

func TestHiddenPlainListingStillListsEverything(t *testing.T) {
	printed := hiddenRun(t)
	for _, invoice := range hiddenInvoices {
		if !strings.Contains(printed, invoice.Number) {
			t.Errorf("%s missing from:\n%s", invoice.Number, printed)
		}
	}
}

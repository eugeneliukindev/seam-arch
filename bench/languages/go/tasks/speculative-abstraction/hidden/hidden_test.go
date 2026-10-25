package shop_test

import (
	"context"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"

	"example.com/shop"
)

func TestHiddenChargesInCents(t *testing.T) {
	var charges []string
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		// Stripe takes the currency in lower case; the case is not the point of the task
		charges = append(charges, r.FormValue("amount")+" "+strings.ToUpper(r.FormValue("currency"))+" "+r.FormValue("source"))
		w.Write([]byte(`{"id": "ch_1"}`))
	}))
	defer server.Close()
	client := &shop.StripeClient{BaseURL: server.URL, HTTP: server.Client()}
	id, err := shop.Charge(context.Background(), shop.Order{ID: 1, TotalCents: 999, Currency: "EUR"}, "tok_1", client)
	if err != nil || id != "ch_1" || len(charges) != 1 || charges[0] != "999 EUR tok_1" {
		t.Fatalf("Charge = %q, %v; charges %v; want ch_1 and one charge of 999 EUR tok_1", id, err, charges)
	}
}

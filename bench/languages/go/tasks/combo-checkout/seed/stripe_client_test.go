package shop_test

import (
	"context"
	"net/http"
	"net/http/httptest"
	"testing"

	"example.com/shop"
)

func TestCreateChargeReturnsTheID(t *testing.T) {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path != "/v1/charges" || r.FormValue("amount") != "500" {
			http.Error(w, "unexpected charge", http.StatusBadRequest)
			return
		}
		w.Write([]byte(`{"id": "ch_9"}`))
	}))
	defer server.Close()
	client := &shop.StripeClient{BaseURL: server.URL, HTTP: server.Client()}
	if id, err := client.CreateCharge(context.Background(), 500, "EUR", "tok_9"); err != nil || id != "ch_9" {
		t.Fatalf("CreateCharge = %q, %v; want ch_9", id, err)
	}
}

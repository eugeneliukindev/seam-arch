package shop_test

import (
	"context"
	"net/http"
	"net/http/httptest"
	"regexp"
	"testing"
	"time"

	"example.com/shop"
)

func hiddenCheckout(t *testing.T, expires time.Time) (*shop.Checkout, *[]string) {
	t.Helper()
	charges := &[]string{}
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		*charges = append(*charges, r.FormValue("amount"))
		w.Write([]byte(`{"id": "ch_1"}`))
	}))
	t.Cleanup(server.Close)
	checkout := shop.BuildCheckout(&shop.StripeClient{BaseURL: server.URL, HTTP: server.Client()})
	checkout.Coupons.Add(shop.Coupon{Code: "TEN", Percent: 10, Expires: expires})
	return checkout, charges
}

func TestHiddenCouponVATAndCharge(t *testing.T) {
	checkout, charges := hiddenCheckout(t, time.Date(2100, 1, 1, 0, 0, 0, 0, time.UTC))
	id, err := checkout.Pay(context.Background(), shop.Cart{TotalCents: 10000}, "TEN", "GB", "tok")
	if err != nil || id != "ch_1" || len(*charges) != 1 || (*charges)[0] != "10800" {
		t.Fatalf("Pay = %q, %v; charges %v; want ch_1 and one charge of 10800", id, err, *charges)
	}
}

func TestHiddenExpiredCouponIsRefused(t *testing.T) {
	checkout, charges := hiddenCheckout(t, time.Date(2000, 1, 1, 0, 0, 0, 0, time.UTC))
	_, err := checkout.Pay(context.Background(), shop.Cart{TotalCents: 10000}, "TEN", "DE", "tok")
	if err == nil || !regexp.MustCompile(`(?i)TEN|expir`).MatchString(err.Error()) || len(*charges) != 0 {
		t.Fatalf("Pay = %v; charges %v; want an expiry error and no charge", err, *charges)
	}
}

package shop_test

import (
	"errors"
	"math"
	"testing"
	"time"

	"example.com/shop"
)

func hiddenBook(expires time.Time) *shop.CouponBook {
	book := shop.BuildBook()
	book.Add(shop.Coupon{Code: "A", Percent: 10, Expires: expires})
	return book
}

func TestHiddenValidCouponLowersTheTotal(t *testing.T) {
	total, err := hiddenBook(time.Date(2100, 1, 1, 0, 0, 0, 0, time.UTC)).Apply("A", 100)
	if err != nil || math.Abs(total-90) > 1e-9 {
		t.Fatalf("Apply = %v, %v; want 90", total, err)
	}
}

func TestHiddenExpiredCouponIsRefused(t *testing.T) {
	_, err := hiddenBook(time.Date(2000, 1, 1, 0, 0, 0, 0, time.UTC)).Apply("A", 100)
	if !errors.Is(err, shop.ErrCouponExpired) {
		t.Fatalf("Apply = %v; want ErrCouponExpired", err)
	}
}

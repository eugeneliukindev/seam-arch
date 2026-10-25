package shop_test

import (
	"testing"
	"time"

	"example.com/shop"
)

func TestAdd(t *testing.T) {
	shop.BuildBook().Add(shop.Coupon{Code: "A", Percent: 10, Expires: time.Date(2100, 1, 1, 0, 0, 0, 0, time.UTC)})
}

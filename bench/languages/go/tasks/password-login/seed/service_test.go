package accounts_test

import (
	"testing"

	"example.com/accounts"
)

func TestUnknownEmailHasNoAccount(t *testing.T) {
	if _, ok := accounts.BuildService().Find("nobody@example.com"); ok {
		t.Fatal("found an account nobody created")
	}
}

package accounts_test

import (
	"testing"

	"example.com/accounts"
)

func hiddenRegistered(t *testing.T) *accounts.AccountService {
	t.Helper()
	service := accounts.BuildService()
	if err := service.Register("a@example.com", "s3cret"); err != nil {
		t.Fatal(err)
	}
	return service
}

func TestHiddenRightPasswordLogsIn(t *testing.T) {
	if ok, err := hiddenRegistered(t).LogIn("a@example.com", "s3cret"); err != nil || !ok {
		t.Fatalf("LogIn = %v, %v; want true", ok, err)
	}
}

func TestHiddenWrongPasswordOrEmailFails(t *testing.T) {
	service := hiddenRegistered(t)
	if ok, _ := service.LogIn("a@example.com", "guess"); ok {
		t.Fatal("logged in with a wrong password")
	}
	if ok, _ := service.LogIn("b@example.com", "s3cret"); ok {
		t.Fatal("logged in to an account nobody created")
	}
	if user, _ := service.Find("a@example.com"); string(user.PasswordHash) == "s3cret" {
		t.Fatal("the password itself is stored")
	}
}

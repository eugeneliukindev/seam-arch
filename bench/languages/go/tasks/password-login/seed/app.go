// Package accounts keeps user accounts.
package accounts

// BuildService returns a ready service with its own store.
func BuildService() *AccountService {
	return NewAccountService(NewInMemoryUsers())
}

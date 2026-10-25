package accounts

// AccountService finds and creates accounts.
type AccountService struct {
	users UserStore
}

// NewAccountService returns a service keeping accounts in users.
func NewAccountService(users UserStore) *AccountService {
	return &AccountService{users: users}
}

// Find returns the account with this email, and whether there is one.
func (s *AccountService) Find(email string) (User, bool) {
	return s.users.Find(email)
}

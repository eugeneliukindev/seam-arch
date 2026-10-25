package accounts

// AccountService finds and creates accounts.
type AccountService struct {
	users  UserStore
	hasher PasswordHasher
}

// NewAccountService returns a service keeping accounts in users and passwords hashed by hasher.
func NewAccountService(users UserStore, hasher PasswordHasher) *AccountService {
	return &AccountService{users: users, hasher: hasher}
}

// Find returns the account with this email, and whether there is one.
func (s *AccountService) Find(email string) (User, bool) {
	return s.users.Find(email)
}

// Register creates an account that logs in with password.
func (s *AccountService) Register(email, password string) error {
	hash, err := s.hasher.Hash(password)
	if err != nil {
		return err
	}
	s.users.Save(User{Email: email, PasswordHash: hash})
	return nil
}

// LogIn reports whether password is the one this account was created with.
func (s *AccountService) LogIn(email, password string) (bool, error) {
	user, ok := s.users.Find(email)
	if !ok {
		return false, nil
	}
	return s.hasher.Verify(password, user.PasswordHash)
}

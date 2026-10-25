package accounts

// User is someone with an account.
type User struct {
	Email        string
	PasswordHash []byte
}

// UserStore is where users are kept.
type UserStore interface {
	// Find returns the user with this email, and whether there is one.
	Find(email string) (User, bool)
	// Save stores user, replacing one with the same email.
	Save(user User)
}

// InMemoryUsers keeps users in a map, for one process.
type InMemoryUsers struct {
	users map[string]User
}

// NewInMemoryUsers returns an empty store.
func NewInMemoryUsers() *InMemoryUsers {
	return &InMemoryUsers{users: map[string]User{}}
}

// Find returns the user with this email, and whether there is one.
func (s *InMemoryUsers) Find(email string) (User, bool) {
	user, ok := s.users[email]
	return user, ok
}

// Save stores user, replacing one with the same email.
func (s *InMemoryUsers) Save(user User) {
	s.users[user.Email] = user
}

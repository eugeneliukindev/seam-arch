package accounts

import (
	"crypto/pbkdf2"
	"crypto/rand"
	"crypto/sha256"
	"crypto/subtle"
	"fmt"
)

const (
	iterations = 600_000
	saltSize   = 16
	keySize    = 32
)

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

// Register creates an account that logs in with password.
func (s *AccountService) Register(email, password string) error {
	salt := make([]byte, saltSize)
	rand.Read(salt)
	digest, err := pbkdf2.Key(sha256.New, password, salt, iterations, keySize)
	if err != nil {
		return fmt.Errorf("hash password: %w", err)
	}
	s.users.Save(User{Email: email, PasswordHash: append(salt, digest...)})
	return nil
}

// LogIn reports whether password is the one this account was created with.
func (s *AccountService) LogIn(email, password string) (bool, error) {
	user, ok := s.users.Find(email)
	if !ok || len(user.PasswordHash) != saltSize+keySize {
		return false, nil
	}
	digest, err := pbkdf2.Key(sha256.New, password, user.PasswordHash[:saltSize], iterations, keySize)
	if err != nil {
		return false, fmt.Errorf("hash password: %w", err)
	}
	return subtle.ConstantTimeCompare(digest, user.PasswordHash[saltSize:]) == 1, nil
}

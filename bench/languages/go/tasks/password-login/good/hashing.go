package accounts

import (
	"crypto/pbkdf2"
	"crypto/rand"
	"crypto/sha256"
	"crypto/subtle"
	"fmt"
)

// PasswordHasher turns a password into a stored hash and checks one against it.
type PasswordHasher interface {
	// Hash returns a new hash of password, different each call.
	Hash(password string) ([]byte, error)
	// Verify reports whether password produced stored.
	Verify(password string, stored []byte) (bool, error)
}

// PBKDF2Hasher is salted PBKDF2 with SHA-256; the salt is stored in front of the digest.
type PBKDF2Hasher struct {
	iterations, saltSize, keySize int
}

// NewPBKDF2Hasher returns a hasher with this many iterations; 600000 is the OWASP advice for SHA-256.
func NewPBKDF2Hasher(iterations int) *PBKDF2Hasher {
	return &PBKDF2Hasher{iterations: iterations, saltSize: 16, keySize: 32}
}

// Hash returns the salt followed by the digest of password.
func (h *PBKDF2Hasher) Hash(password string) ([]byte, error) {
	salt := make([]byte, h.saltSize)
	rand.Read(salt)
	digest, err := h.digest(password, salt)
	if err != nil {
		return nil, err
	}
	return append(salt, digest...), nil
}

// Verify reports whether password produced stored.
func (h *PBKDF2Hasher) Verify(password string, stored []byte) (bool, error) {
	if len(stored) != h.saltSize+h.keySize {
		return false, nil
	}
	digest, err := h.digest(password, stored[:h.saltSize])
	if err != nil {
		return false, err
	}
	return subtle.ConstantTimeCompare(digest, stored[h.saltSize:]) == 1, nil
}

func (h *PBKDF2Hasher) digest(password string, salt []byte) ([]byte, error) {
	digest, err := pbkdf2.Key(sha256.New, password, salt, h.iterations, h.keySize)
	if err != nil {
		return nil, fmt.Errorf("hash password: %w", err)
	}
	return digest, nil
}

//! Password hashing: the contract and its implementations.

use crate::kdf;

/// Turns a password into a stored hash and checks one against it.
pub trait PasswordHasher {
    /// A new hash of `password`, different each call.
    fn hash(&self, password: &str) -> Vec<u8>;

    /// Whether `password` produced `stored`.
    fn verify(&self, password: &str, stored: &[u8]) -> bool;
}

/// `kdf::derive` with a random salt stored in front of the key.
pub struct KdfHasher;

const SALT_LEN: usize = 16;

impl PasswordHasher for KdfHasher {
    fn hash(&self, password: &str) -> Vec<u8> {
        let mut stored = kdf::random_salt();
        stored.extend(kdf::derive(password, &stored));
        stored
    }

    fn verify(&self, password: &str, stored: &[u8]) -> bool {
        if stored.len() < SALT_LEN {
            return false;
        }
        let (salt, key) = stored.split_at(SALT_LEN);
        let candidate = kdf::derive(password, salt);
        // constant time: the comparison must not tell how many bytes matched
        candidate.len() == key.len() && candidate.iter().zip(key).fold(0, |diff, (a, b)| diff | (a ^ b)) == 0
    }
}

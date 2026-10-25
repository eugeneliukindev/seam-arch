//! What can be done with an account.

use crate::kdf::{derive, random_salt};
use crate::users::{User, UserStore};

const SALT_LEN: usize = 16;

/// Finds and creates accounts.
pub struct AccountService {
    users: Box<dyn UserStore>,
}

impl AccountService {
    pub fn new(users: Box<dyn UserStore>) -> Self {
        Self { users }
    }

    /// The account with this email, or `None`.
    pub fn find(&self, email: &str) -> Option<&User> {
        self.users.find(email)
    }

    /// Create an account that logs in with `password`.
    pub fn register(&mut self, email: &str, password: &str) {
        let mut password_hash = random_salt();
        password_hash.extend(derive(password, &password_hash));
        self.users.save(User { email: email.to_owned(), password_hash });
    }

    /// Whether `password` is the one this account was created with.
    pub fn log_in(&self, email: &str, password: &str) -> bool {
        let Some(user) = self.users.find(email) else {
            return false;
        };
        let (salt, key) = user.password_hash.split_at(SALT_LEN.min(user.password_hash.len()));
        derive(password, salt) == key
    }
}

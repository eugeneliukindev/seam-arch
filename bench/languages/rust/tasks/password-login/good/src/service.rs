//! What can be done with an account.

use crate::hashing::PasswordHasher;
use crate::users::{User, UserStore};

/// Finds and creates accounts.
pub struct AccountService {
    users: Box<dyn UserStore>,
    hasher: Box<dyn PasswordHasher>,
}

impl AccountService {
    pub fn new(users: Box<dyn UserStore>, hasher: Box<dyn PasswordHasher>) -> Self {
        Self { users, hasher }
    }

    /// The account with this email, or `None`.
    pub fn find(&self, email: &str) -> Option<&User> {
        self.users.find(email)
    }

    /// Create an account that logs in with `password`.
    pub fn register(&mut self, email: &str, password: &str) {
        let password_hash = self.hasher.hash(password);
        self.users.save(User { email: email.to_owned(), password_hash });
    }

    /// Whether `password` is the one this account was created with.
    pub fn log_in(&self, email: &str, password: &str) -> bool {
        self.users.find(email).is_some_and(|user| self.hasher.verify(password, &user.password_hash))
    }
}

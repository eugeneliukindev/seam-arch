//! Users and where they are kept.

use std::collections::HashMap;

/// Someone with an account.
#[derive(Debug, Clone, Default, PartialEq, Eq)]
pub struct User {
    pub email: String,
    pub password_hash: Vec<u8>,
}

/// Where users are kept.
pub trait UserStore {
    /// The user with this email, or `None`.
    fn find(&self, email: &str) -> Option<&User>;

    /// Store `user`, replacing one with the same email.
    fn save(&mut self, user: User);
}

/// Users kept in a map, for one process.
#[derive(Debug, Default)]
pub struct InMemoryUsers {
    users: HashMap<String, User>,
}

impl UserStore for InMemoryUsers {
    fn find(&self, email: &str) -> Option<&User> {
        self.users.get(email)
    }

    fn save(&mut self, user: User) {
        self.users.insert(user.email.clone(), user);
    }
}

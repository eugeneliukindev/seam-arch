//! What can be done with an account.

use crate::users::{User, UserStore};

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
}

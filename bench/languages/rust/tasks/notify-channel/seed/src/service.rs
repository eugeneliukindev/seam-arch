//! Raising alerts.

use crate::email::EmailNotifier;
use crate::users::User;

/// Raises alerts for users.
pub struct AlertService {
    notifier: EmailNotifier,
}

impl AlertService {
    pub fn new(notifier: EmailNotifier) -> Self {
        Self { notifier }
    }

    /// Deliver `text` to `user`.
    pub fn alert(&self, user: &User, text: &str) {
        self.notifier.notify(user, text);
    }
}

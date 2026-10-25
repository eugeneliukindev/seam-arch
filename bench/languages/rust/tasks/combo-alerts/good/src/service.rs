//! Raising alerts.

use std::collections::HashMap;
use std::error::Error;
use std::fmt;

use crate::users::{Channel, User};

/// An alert that could not be delivered.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum AlertError {
    /// No notifier was built for the user's channel.
    NoNotifier { user: u64 },
}

impl fmt::Display for AlertError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::NoNotifier { user } => write!(formatter, "no notifier for the channel of user {user}"),
        }
    }
}

impl Error for AlertError {}

/// Delivers an alert by one channel.
pub trait Notifier {
    /// Deliver `text` to `user`.
    fn notify(&self, user: &User, text: &str) -> Result<(), AlertError>;
}

/// Raises alerts for users, each by the channel they chose.
pub struct AlertService {
    notifiers: HashMap<Channel, Box<dyn Notifier>>,
}

impl AlertService {
    pub fn new(notifiers: HashMap<Channel, Box<dyn Notifier>>) -> Self {
        Self { notifiers }
    }

    /// Deliver `text` to `user`.
    pub fn alert(&self, user: &User, text: &str) -> Result<(), AlertError> {
        let notifier = self.notifiers.get(&user.channel).ok_or(AlertError::NoNotifier { user: user.id })?;
        notifier.notify(user, text)
    }
}

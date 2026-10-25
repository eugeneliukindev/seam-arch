//! Raising alerts.

use std::rc::Rc;

use crate::email::EmailNotifier;
use crate::gateways::SmsGateway;
use crate::users::{Channel, User};

/// Raises alerts for users.
pub struct AlertService {
    notifier: EmailNotifier,
    sms: Rc<dyn SmsGateway>,
}

impl AlertService {
    pub fn new(notifier: EmailNotifier, sms: Rc<dyn SmsGateway>) -> Self {
        Self { notifier, sms }
    }

    /// Deliver `text` to `user`.
    pub fn alert(&self, user: &User, text: &str) {
        match (user.channel, &user.phone) {
            (Channel::Sms, Some(phone)) => self.sms.send(phone, text),
            _ => self.notifier.notify(user, text),
        }
    }
}

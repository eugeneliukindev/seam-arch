//! Raising alerts.

use std::rc::Rc;

use crate::email::EmailNotifier;
use crate::gateways::{PushGateway, SmsGateway};
use crate::users::{Channel, User};

/// Raises alerts for users.
pub struct AlertService {
    notifier: EmailNotifier,
    sms: Rc<dyn SmsGateway>,
    push: Rc<dyn PushGateway>,
}

impl AlertService {
    pub fn new(notifier: EmailNotifier, sms: Rc<dyn SmsGateway>, push: Rc<dyn PushGateway>) -> Self {
        Self { notifier, sms, push }
    }

    /// Deliver `text` to `user`.
    pub fn alert(&self, user: &User, text: &str) {
        match (user.channel, &user.phone, &user.device_token) {
            (Channel::Sms, Some(phone), _) => self.sms.send(phone, text),
            (Channel::Push, _, Some(device)) => self.push.send(device, text),
            _ => self.notifier.notify(user, text),
        }
    }
}

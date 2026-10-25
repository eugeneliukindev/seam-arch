//! Alerts delivered by text message.

use std::rc::Rc;

use crate::gateways::SmsGateway;
use crate::service::{AlertError, Notifier};
use crate::users::User;

/// Delivers an alert to a user's phone, or by the fallback when there is no phone.
pub struct SmsNotifier {
    gateway: Rc<dyn SmsGateway>,
    fallback: Box<dyn Notifier>,
}

impl SmsNotifier {
    pub fn new(gateway: Rc<dyn SmsGateway>, fallback: Box<dyn Notifier>) -> Self {
        Self { gateway, fallback }
    }
}

impl Notifier for SmsNotifier {
    /// Text `text` to `user`.
    fn notify(&self, user: &User, text: &str) -> Result<(), AlertError> {
        match user.phone.as_deref() {
            Some(phone) => {
                self.gateway.send(phone, text);
                Ok(())
            }
            None => self.fallback.notify(user, text),
        }
    }
}

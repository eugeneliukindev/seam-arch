//! Alerts delivered by text message.

use std::rc::Rc;

use crate::gateways::SmsGateway;
use crate::service::{AlertError, Notifier};
use crate::users::User;

/// Delivers an alert to a user's phone.
pub struct SmsNotifier {
    gateway: Rc<dyn SmsGateway>,
}

impl SmsNotifier {
    pub fn new(gateway: Rc<dyn SmsGateway>) -> Self {
        Self { gateway }
    }
}

impl Notifier for SmsNotifier {
    /// Text `text` to `user`.
    fn notify(&self, user: &User, text: &str) -> Result<(), AlertError> {
        let phone = user.phone.as_deref().ok_or(AlertError::NoPhone { user: user.id })?;
        self.gateway.send(phone, text);
        Ok(())
    }
}

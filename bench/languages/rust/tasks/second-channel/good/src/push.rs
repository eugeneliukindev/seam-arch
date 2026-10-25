//! Alerts delivered to the phone app.

use std::rc::Rc;

use crate::gateways::PushGateway;
use crate::service::{AlertError, Notifier};
use crate::users::User;

/// Delivers an alert to a user's phone app.
pub struct PushNotifier {
    gateway: Rc<dyn PushGateway>,
}

impl PushNotifier {
    pub fn new(gateway: Rc<dyn PushGateway>) -> Self {
        Self { gateway }
    }
}

impl Notifier for PushNotifier {
    /// Push `text` to `user`'s app.
    fn notify(&self, user: &User, text: &str) -> Result<(), AlertError> {
        let device = user.device_token.as_deref().ok_or(AlertError::NoAddress { user: user.id })?;
        self.gateway.send(device, text);
        Ok(())
    }
}

//! Alerts delivered to the phone app.

use std::rc::Rc;

use crate::gateways::PushGateway;
use crate::service::{AlertError, Notifier};
use crate::users::User;

/// Delivers an alert to a user's phone app, or by the fallback when there is no device.
pub struct PushNotifier {
    gateway: Rc<dyn PushGateway>,
    fallback: Box<dyn Notifier>,
}

impl PushNotifier {
    pub fn new(gateway: Rc<dyn PushGateway>, fallback: Box<dyn Notifier>) -> Self {
        Self { gateway, fallback }
    }
}

impl Notifier for PushNotifier {
    /// Push `text` to `user`'s app.
    fn notify(&self, user: &User, text: &str) -> Result<(), AlertError> {
        match user.device_token.as_deref() {
            Some(device) => {
                self.gateway.send(device, text);
                Ok(())
            }
            None => self.fallback.notify(user, text),
        }
    }
}

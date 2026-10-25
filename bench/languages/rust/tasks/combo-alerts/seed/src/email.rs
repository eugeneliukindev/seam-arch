//! Alerts delivered by mail.

use std::rc::Rc;

use crate::gateways::SmtpClient;
use crate::users::User;

/// Delivers an alert to a user's mailbox.
pub struct EmailNotifier {
    smtp: Rc<dyn SmtpClient>,
}

impl EmailNotifier {
    pub fn new(smtp: Rc<dyn SmtpClient>) -> Self {
        Self { smtp }
    }

    /// Mail `text` to `user`.
    pub fn notify(&self, user: &User, text: &str) {
        self.smtp.send_mail(&user.email, "Alert", text);
    }
}

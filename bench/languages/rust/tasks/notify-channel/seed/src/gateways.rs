//! Clients of the services that deliver messages; configured in production.

/// Sends mail through the mail relay.
pub trait SmtpClient {
    /// Hand one message to the relay.
    fn send_mail(&self, to: &str, subject: &str, body: &str);
}

/// Sends text messages through the SMS provider.
pub trait SmsGateway {
    /// Hand one text message to the provider.
    fn send(&self, phone: &str, text: &str);
}

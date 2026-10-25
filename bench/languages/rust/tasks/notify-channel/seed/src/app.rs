//! Builds the alert service from the delivery clients.

use std::rc::Rc;

use crate::email::EmailNotifier;
use crate::gateways::{SmsGateway, SmtpClient};
use crate::service::AlertService;

/// The alert service the application uses.
pub fn build_service(smtp: Rc<dyn SmtpClient>, _sms: Rc<dyn SmsGateway>) -> AlertService {
    AlertService::new(EmailNotifier::new(smtp))
}

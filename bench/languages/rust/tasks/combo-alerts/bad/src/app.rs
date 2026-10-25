//! Builds the alert service from the delivery clients.

use std::rc::Rc;

use crate::email::EmailNotifier;
use crate::gateways::{PushGateway, SmsGateway, SmtpClient};
use crate::service::AlertService;

/// The alert service the application uses.
pub fn build_service(smtp: Rc<dyn SmtpClient>, sms: Rc<dyn SmsGateway>, push: Rc<dyn PushGateway>) -> AlertService {
    AlertService::new(EmailNotifier::new(smtp), sms, push)
}

//! Builds the alert service from the delivery clients.

use std::collections::HashMap;
use std::rc::Rc;

use crate::email::EmailNotifier;
use crate::gateways::{PushGateway, SmsGateway, SmtpClient};
use crate::push::PushNotifier;
use crate::service::{AlertService, Notifier};
use crate::sms::SmsNotifier;
use crate::users::Channel;

/// The alert service the application uses.
pub fn build_service(smtp: Rc<dyn SmtpClient>, sms: Rc<dyn SmsGateway>, push: Rc<dyn PushGateway>) -> AlertService {
    let email = || Box::new(EmailNotifier::new(smtp.clone())) as Box<dyn Notifier>;
    let notifiers: HashMap<Channel, Box<dyn Notifier>> = HashMap::from([
        (Channel::Email, email()),
        (Channel::Sms, Box::new(SmsNotifier::new(sms, email())) as Box<dyn Notifier>),
        (Channel::Push, Box::new(PushNotifier::new(push, email()))),
    ]);
    AlertService::new(notifiers)
}

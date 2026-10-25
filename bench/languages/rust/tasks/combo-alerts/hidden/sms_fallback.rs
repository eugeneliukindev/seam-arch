use std::cell::RefCell;
use std::rc::Rc;

use alerts::app::build_service;
use alerts::gateways::{PushGateway, SmsGateway, SmtpClient};
use alerts::users::{Channel, User};

#[derive(Default)]
pub struct FakeSmtp {
    pub sent: RefCell<Vec<String>>,
}

impl SmtpClient for FakeSmtp {
    fn send_mail(&self, to: &str, _subject: &str, _body: &str) {
        self.sent.borrow_mut().push(to.to_owned());
    }
}

#[derive(Default)]
pub struct FakeSms {
    pub sent: RefCell<Vec<String>>,
}

impl SmsGateway for FakeSms {
    fn send(&self, phone: &str, _text: &str) {
        self.sent.borrow_mut().push(phone.to_owned());
    }
}

#[derive(Default)]
pub struct FakePush {
    pub sent: RefCell<Vec<String>>,
}

impl PushGateway for FakePush {
    fn send(&self, device_token: &str, _text: &str) {
        self.sent.borrow_mut().push(device_token.to_owned());
    }
}

#[test]
fn sms_without_phone_falls_back_to_mail() {
    let (smtp, sms, push) = (Rc::new(FakeSmtp::default()), Rc::new(FakeSms::default()), Rc::new(FakePush::default()));
    let service = build_service(smtp.clone(), sms.clone(), push.clone());
    let user = User { id: 3, email: "c@example.com".into(), phone: None, device_token: None, channel: Channel::Sms };
    let _ = service.alert(&user, "disk full");
    assert_eq!(*smtp.sent.borrow(), vec!["c@example.com".to_owned()]);
    assert!(sms.sent.borrow().is_empty() && push.sent.borrow().is_empty());
}

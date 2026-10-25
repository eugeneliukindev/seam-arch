use std::cell::RefCell;
use std::rc::Rc;

use alerts::app::build_service;
use alerts::gateways::{SmsGateway, SmtpClient};
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

#[test]
fn sms_user_gets_a_text() {
    let (smtp, sms) = (Rc::new(FakeSmtp::default()), Rc::new(FakeSms::default()));
    let service = build_service(smtp.clone(), sms.clone());
    let user = User { id: 1, email: "a@example.com".into(), phone: Some("+100".into()), channel: Channel::Sms };
    let _ = service.alert(&user, "disk full");
    assert_eq!(*sms.sent.borrow(), vec!["+100".to_owned()]);
    assert!(smtp.sent.borrow().is_empty());
}

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
fn email_user_gets_mail() {
    let (smtp, sms) = (Rc::new(FakeSmtp::default()), Rc::new(FakeSms::default()));
    let service = build_service(smtp.clone(), sms.clone());
    let user = User { id: 2, email: "b@example.com".into(), phone: Some("+200".into()), channel: Channel::Email };
    let _ = service.alert(&user, "disk full");
    assert_eq!(*smtp.sent.borrow(), vec!["b@example.com".to_owned()]);
    assert!(sms.sent.borrow().is_empty());
}

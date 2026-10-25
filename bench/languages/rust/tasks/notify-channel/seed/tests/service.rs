use std::cell::RefCell;
use std::rc::Rc;

use alerts::app::build_service;
use alerts::gateways::{SmsGateway, SmtpClient};
use alerts::users::User;

#[derive(Default)]
struct FakeSmtp {
    sent: RefCell<Vec<(String, String)>>,
}

impl SmtpClient for FakeSmtp {
    fn send_mail(&self, to: &str, _subject: &str, body: &str) {
        self.sent.borrow_mut().push((to.to_owned(), body.to_owned()));
    }
}

struct NoSms;

impl SmsGateway for NoSms {
    fn send(&self, _phone: &str, _text: &str) {
        panic!("no text messages in this test");
    }
}

#[test]
fn alert_by_mail() {
    let smtp = Rc::new(FakeSmtp::default());
    let user = User { id: 1, email: "a@example.com".into(), ..User::default() };
    let _ = build_service(smtp.clone(), Rc::new(NoSms)).alert(&user, "disk full");
    assert_eq!(*smtp.sent.borrow(), vec![("a@example.com".to_owned(), "disk full".to_owned())]);
}

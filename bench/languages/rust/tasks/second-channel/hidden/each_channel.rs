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
fn each_channel_delivers() {
    for (channel, pick) in [(Channel::Email, 0), (Channel::Sms, 1), (Channel::Push, 2)] {
        let (smtp, sms, push) = (Rc::new(FakeSmtp::default()), Rc::new(FakeSms::default()), Rc::new(FakePush::default()));
        let service = build_service(smtp.clone(), sms.clone(), push.clone());
        let user = User {
            id: 1,
            email: "a@example.com".into(),
            phone: Some("+100".into()),
            device_token: Some("dev-1".into()),
            channel,
        };
        let _ = service.alert(&user, "disk full");
        let counts = [smtp.sent.borrow().len(), sms.sent.borrow().len(), push.sent.borrow().len()];
        let expected: Vec<usize> = (0..3).map(|sink| usize::from(sink == pick)).collect();
        assert_eq!(counts.to_vec(), expected, "{channel:?}");
    }
}

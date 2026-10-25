package alerts_test

import (
	"slices"
	"testing"

	"example.com/alerts"
)

type hiddenSmtp struct{ sent []string }

func (f *hiddenSmtp) SendMail(to, subject, body string) error {
	f.sent = append(f.sent, to)
	return nil
}

type hiddenSms struct{ sent []string }

func (f *hiddenSms) Send(phone, text string) error {
	f.sent = append(f.sent, phone)
	return nil
}

func hiddenAlert(t *testing.T, user alerts.User) (mails, texts []string) {
	t.Helper()
	smtp, sms := &hiddenSmtp{}, &hiddenSms{}
	if err := alerts.BuildService(smtp, sms).Alert(user, "disk full"); err != nil {
		t.Fatal(err)
	}
	return smtp.sent, sms.sent
}

func TestHiddenSmsUserGetsAText(t *testing.T) {
	mails, texts := hiddenAlert(t, alerts.User{ID: 1, Email: "a@example.com", Phone: "+100", Channel: "sms"})
	if len(mails) != 0 || !slices.Equal(texts, []string{"+100"}) {
		t.Fatalf("mails %v, texts %v; want one text to +100", mails, texts)
	}
}

func TestHiddenEmailUserGetsMail(t *testing.T) {
	mails, texts := hiddenAlert(t, alerts.User{ID: 2, Email: "b@example.com", Phone: "+200", Channel: "email"})
	if len(texts) != 0 || !slices.Equal(mails, []string{"b@example.com"}) {
		t.Fatalf("mails %v, texts %v; want one mail to b@example.com", mails, texts)
	}
}

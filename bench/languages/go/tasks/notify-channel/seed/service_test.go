package alerts_test

import (
	"testing"

	"example.com/alerts"
)

type fakeSmtp struct{ sent []string }

func (f *fakeSmtp) SendMail(to, subject, body string) error {
	f.sent = append(f.sent, to+": "+body)
	return nil
}

type unusedSms struct{}

func (unusedSms) Send(phone, text string) error { panic("no texts expected") }

func TestAlertByMail(t *testing.T) {
	smtp := &fakeSmtp{}
	if err := alerts.BuildService(smtp, unusedSms{}).Alert(alerts.User{ID: 1, Email: "a@example.com"}, "disk full"); err != nil {
		t.Fatal(err)
	}
	if len(smtp.sent) != 1 || smtp.sent[0] != "a@example.com: disk full" {
		t.Fatalf("sent = %v", smtp.sent)
	}
}

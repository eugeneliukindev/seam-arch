package alerts_test

import (
	"testing"

	"example.com/alerts"
)

type hiddenSink struct{ sent []string }

func (f *hiddenSink) SendMail(to, subject, body string) error {
	f.sent = append(f.sent, to)
	return nil
}

func (f *hiddenSink) Send(address, text string) error {
	f.sent = append(f.sent, address)
	return nil
}

// hiddenAlert alerts user and returns how many mails, texts and notifications went out, and the mail recipients.
func hiddenAlert(t *testing.T, user alerts.User) ([3]int, []string) {
	t.Helper()
	smtp, sms, push := &hiddenSink{}, &hiddenSink{}, &hiddenSink{}
	if err := alerts.BuildService(smtp, sms, push).Alert(user, "disk full"); err != nil {
		t.Fatal(err)
	}
	return [3]int{len(smtp.sent), len(sms.sent), len(push.sent)}, smtp.sent
}

func TestHiddenEachChannelDelivers(t *testing.T) {
	users := []alerts.User{
		{ID: 1, Email: "a@example.com", Phone: "+100", DeviceToken: "dev-1", Channel: "email"},
		{ID: 1, Email: "a@example.com", Phone: "+100", DeviceToken: "dev-1", Channel: "sms"},
		{ID: 1, Email: "a@example.com", Phone: "+100", DeviceToken: "dev-1", Channel: "push"},
	}
	for i, user := range users {
		want := [3]int{}
		want[i] = 1
		if got, _ := hiddenAlert(t, user); got != want {
			t.Errorf("channel %v: mails, texts, pushes = %v; want %v", user.Channel, got, want)
		}
	}
}

package alerts

import "fmt"

// SmsNotifier delivers an alert to a user's phone.
type SmsNotifier struct {
	gateway SmsGateway
}

// NewSmsNotifier returns a notifier texting through gateway.
func NewSmsNotifier(gateway SmsGateway) *SmsNotifier {
	return &SmsNotifier{gateway: gateway}
}

// Notify texts text to user.
func (n *SmsNotifier) Notify(user User, text string) error {
	if user.Phone == "" {
		return fmt.Errorf("user %d chose text messages but has no phone", user.ID)
	}
	return n.gateway.Send(user.Phone, text)
}

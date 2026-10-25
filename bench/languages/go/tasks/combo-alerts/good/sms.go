package alerts

// SmsNotifier delivers an alert to a user's phone, or by the fallback when there is no phone.
type SmsNotifier struct {
	gateway  SmsGateway
	fallback Notifier
}

// NewSmsNotifier returns a notifier texting through gateway, and delivering by fallback to users without a phone.
func NewSmsNotifier(gateway SmsGateway, fallback Notifier) *SmsNotifier {
	return &SmsNotifier{gateway: gateway, fallback: fallback}
}

// Notify texts text to user.
func (n *SmsNotifier) Notify(user User, text string) error {
	if user.Phone == "" {
		return n.fallback.Notify(user, text)
	}
	return n.gateway.Send(user.Phone, text)
}

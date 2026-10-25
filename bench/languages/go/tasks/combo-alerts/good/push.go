package alerts

// PushNotifier delivers an alert to a user's phone app, or by the fallback when there is no device.
type PushNotifier struct {
	gateway  PushGateway
	fallback Notifier
}

// NewPushNotifier returns a notifier pushing through gateway, and delivering by fallback to users without a device.
func NewPushNotifier(gateway PushGateway, fallback Notifier) *PushNotifier {
	return &PushNotifier{gateway: gateway, fallback: fallback}
}

// Notify pushes text to user's app.
func (n *PushNotifier) Notify(user User, text string) error {
	if user.DeviceToken == "" {
		return n.fallback.Notify(user, text)
	}
	return n.gateway.Send(user.DeviceToken, text)
}

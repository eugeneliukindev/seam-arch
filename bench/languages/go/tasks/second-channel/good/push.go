package alerts

import "fmt"

// PushNotifier delivers an alert to a user's phone app.
type PushNotifier struct {
	gateway PushGateway
}

// NewPushNotifier returns a notifier pushing through gateway.
func NewPushNotifier(gateway PushGateway) *PushNotifier {
	return &PushNotifier{gateway: gateway}
}

// Notify pushes text to user's app.
func (n *PushNotifier) Notify(user User, text string) error {
	if user.DeviceToken == "" {
		return fmt.Errorf("user %d chose push but has no device", user.ID)
	}
	return n.gateway.Send(user.DeviceToken, text)
}

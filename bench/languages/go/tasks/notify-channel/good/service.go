package alerts

import "fmt"

// Notifier delivers an alert by one channel.
type Notifier interface {
	Notify(user User, text string) error
}

// AlertService raises alerts for users, each by the channel they chose.
type AlertService struct {
	notifiers map[Channel]Notifier
}

// NewAlertService returns a service delivering by the notifier of each user's channel.
func NewAlertService(notifiers map[Channel]Notifier) *AlertService {
	return &AlertService{notifiers: notifiers}
}

// Alert delivers text to user.
func (s *AlertService) Alert(user User, text string) error {
	notifier, ok := s.notifiers[user.Channel]
	if !ok {
		return fmt.Errorf("user %d: no notifier for channel %q", user.ID, user.Channel)
	}
	return notifier.Notify(user, text)
}

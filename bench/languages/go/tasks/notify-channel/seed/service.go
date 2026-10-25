package alerts

// AlertService raises alerts for users.
type AlertService struct {
	notifier *EmailNotifier
}

// NewAlertService returns a service delivering through notifier.
func NewAlertService(notifier *EmailNotifier) *AlertService {
	return &AlertService{notifier: notifier}
}

// Alert delivers text to user.
func (s *AlertService) Alert(user User, text string) error {
	return s.notifier.Notify(user, text)
}

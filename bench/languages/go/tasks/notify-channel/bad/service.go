package alerts

// AlertService raises alerts for users.
type AlertService struct {
	notifier *EmailNotifier
	sms      SmsGateway
}

// NewAlertService returns a service delivering through notifier, or sms for users who chose it.
func NewAlertService(notifier *EmailNotifier, sms SmsGateway) *AlertService {
	return &AlertService{notifier: notifier, sms: sms}
}

// Alert delivers text to user.
func (s *AlertService) Alert(user User, text string) error {
	if user.Channel == ChannelSMS && user.Phone != "" {
		return s.sms.Send(user.Phone, text)
	}
	return s.notifier.Notify(user, text)
}

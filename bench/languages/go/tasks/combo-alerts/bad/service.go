package alerts

// AlertService raises alerts for users.
type AlertService struct {
	notifier *EmailNotifier
	sms      SmsGateway
	push     PushGateway
}

// NewAlertService returns a service delivering through notifier, or sms or push for users who chose them.
func NewAlertService(notifier *EmailNotifier, sms SmsGateway, push PushGateway) *AlertService {
	return &AlertService{notifier: notifier, sms: sms, push: push}
}

// Alert delivers text to user.
func (s *AlertService) Alert(user User, text string) error {
	if user.Channel == ChannelSMS && user.Phone != "" {
		return s.sms.Send(user.Phone, text)
	}
	if user.Channel == ChannelPush && user.DeviceToken != "" {
		return s.push.Send(user.DeviceToken, text)
	}
	return s.notifier.Notify(user, text)
}

// Package alerts delivers alerts to our users.
package alerts

// BuildService returns the alert service the application uses.
func BuildService(smtp SmtpClient, sms SmsGateway) *AlertService {
	email := NewEmailNotifier(smtp)
	return NewAlertService(map[Channel]Notifier{"": email, ChannelEmail: email, ChannelSMS: NewSmsNotifier(sms)})
}

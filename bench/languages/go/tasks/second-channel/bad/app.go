// Package alerts delivers alerts to our users.
package alerts

// BuildService returns the alert service the application uses.
func BuildService(smtp SmtpClient, sms SmsGateway, push PushGateway) *AlertService {
	return NewAlertService(NewEmailNotifier(smtp), sms, push)
}

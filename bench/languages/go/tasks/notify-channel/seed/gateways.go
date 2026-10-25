package alerts

// SmtpClient sends mail through the mail relay; production configures it.
type SmtpClient interface {
	// SendMail hands one message to the relay.
	SendMail(to, subject, body string) error
}

// SmsGateway sends text messages through the SMS provider; production configures it.
type SmsGateway interface {
	// Send hands one text message to the provider.
	Send(phone, text string) error
}

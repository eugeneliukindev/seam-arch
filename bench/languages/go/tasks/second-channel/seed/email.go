package alerts

// EmailNotifier delivers an alert to a user's mailbox.
type EmailNotifier struct {
	smtp SmtpClient
}

// NewEmailNotifier returns a notifier mailing through smtp.
func NewEmailNotifier(smtp SmtpClient) *EmailNotifier {
	return &EmailNotifier{smtp: smtp}
}

// Notify mails text to user.
func (n *EmailNotifier) Notify(user User, text string) error {
	return n.smtp.SendMail(user.Email, "Alert", text)
}

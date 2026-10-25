package alerts;

/** Delivers an alert to a user's mailbox. */
public final class EmailNotifier {
    private final SmtpClient smtp;

    public EmailNotifier(SmtpClient smtp) {
        this.smtp = smtp;
    }

    /** Mail {@code text} to {@code user}. */
    public void deliver(User user, String text) {
        smtp.sendMail(user.email(), "Alert", text);
    }
}

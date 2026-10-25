package alerts;

/** Sends mail through the mail relay. */
public class SmtpClient {
    /** Hand one message to the relay. */
    public void sendMail(String to, String subject, String body) {
        throw new UnsupportedOperationException("the relay is configured in production");
    }
}

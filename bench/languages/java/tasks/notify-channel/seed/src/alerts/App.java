package alerts;

/** Builds the alert service from the delivery clients. */
public final class App {
    private App() {
    }

    /** The alert service the application uses. */
    public static AlertService buildService(SmtpClient smtp, SmsGateway sms) {
        return new AlertService(new EmailNotifier(smtp));
    }
}

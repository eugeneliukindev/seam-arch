package alerts;

import java.util.Map;

/** Builds the alert service from the delivery clients. */
public final class App {
    private App() {
    }

    /** The alert service the application uses. */
    public static AlertService buildService(SmtpClient smtp, SmsGateway sms) {
        return new AlertService(Map.of(Channel.EMAIL, new EmailNotifier(smtp), Channel.SMS, new SmsNotifier(sms)));
    }
}

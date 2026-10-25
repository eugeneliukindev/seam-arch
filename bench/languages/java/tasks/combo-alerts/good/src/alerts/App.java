package alerts;

import java.util.Map;

/** Builds the alert service from the delivery clients. */
public final class App {
    private App() {
    }

    /** The alert service the application uses. */
    public static AlertService buildService(SmtpClient smtp, SmsGateway sms, PushGateway push) {
        Notifier email = new EmailNotifier(smtp);
        return new AlertService(Map.of(
            Channel.EMAIL, email, Channel.SMS, new SmsNotifier(sms, email), Channel.PUSH, new PushNotifier(push, email)));
    }
}

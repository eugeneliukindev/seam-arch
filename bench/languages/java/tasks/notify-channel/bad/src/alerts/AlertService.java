package alerts;

/** Raises alerts for users. */
public final class AlertService {
    private final EmailNotifier notifier;
    private final SmsGateway sms;

    public AlertService(EmailNotifier notifier, SmsGateway sms) {
        this.notifier = notifier;
        this.sms = sms;
    }

    /** Deliver {@code text} to {@code user}. */
    public void alert(User user, String text) {
        if (user.channel() == Channel.SMS && user.phone() != null) {
            sms.send(user.phone(), text);
        } else {
            notifier.deliver(user, text);
        }
    }
}

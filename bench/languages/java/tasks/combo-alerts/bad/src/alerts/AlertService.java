package alerts;

/** Raises alerts for users. */
public final class AlertService {
    private final EmailNotifier notifier;
    private final SmsGateway sms;
    private final PushGateway push;

    public AlertService(EmailNotifier notifier, SmsGateway sms, PushGateway push) {
        this.notifier = notifier;
        this.sms = sms;
        this.push = push;
    }

    /** Deliver {@code text} to {@code user}. */
    public void alert(User user, String text) {
        if (user.channel() == Channel.SMS && user.phone() != null) {
            sms.send(user.phone(), text);
        } else if (user.channel() == Channel.PUSH && user.deviceToken() != null) {
            push.send(user.deviceToken(), text);
        } else {
            notifier.deliver(user, text);
        }
    }
}

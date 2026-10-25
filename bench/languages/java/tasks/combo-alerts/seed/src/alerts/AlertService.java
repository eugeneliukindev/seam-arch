package alerts;

/** Raises alerts for users. */
public final class AlertService {
    private final EmailNotifier notifier;

    public AlertService(EmailNotifier notifier) {
        this.notifier = notifier;
    }

    /** Deliver {@code text} to {@code user}. */
    public void alert(User user, String text) {
        notifier.deliver(user, text);
    }
}

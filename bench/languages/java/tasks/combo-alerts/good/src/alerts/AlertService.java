package alerts;

import java.util.Map;

/** Raises alerts for users, each by the channel they chose. */
public final class AlertService {
    private final Map<Channel, Notifier> notifiers;

    public AlertService(Map<Channel, Notifier> notifiers) {
        this.notifiers = Map.copyOf(notifiers);
    }

    /** Deliver {@code text} to {@code user}. */
    public void alert(User user, String text) {
        notifiers.get(user.channel()).deliver(user, text);
    }
}

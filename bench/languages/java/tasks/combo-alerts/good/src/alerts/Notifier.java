package alerts;

/** Delivers an alert by one channel. */
public interface Notifier {
    /** Deliver {@code text} to {@code user}. */
    void deliver(User user, String text);
}

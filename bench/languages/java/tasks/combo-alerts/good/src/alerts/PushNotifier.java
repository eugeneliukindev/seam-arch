package alerts;

/** Delivers an alert to a user's phone app, or by the fallback when there is no device. */
public final class PushNotifier implements Notifier {
    private final PushGateway gateway;
    private final Notifier fallback;

    public PushNotifier(PushGateway gateway, Notifier fallback) {
        this.gateway = gateway;
        this.fallback = fallback;
    }

    @Override
    public void deliver(User user, String text) {
        if (user.deviceToken() == null) {
            fallback.deliver(user, text);
            return;
        }
        gateway.send(user.deviceToken(), text);
    }
}

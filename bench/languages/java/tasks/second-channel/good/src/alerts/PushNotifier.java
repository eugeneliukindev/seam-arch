package alerts;

/** Delivers an alert to a user's phone app. */
public final class PushNotifier implements Notifier {
    private final PushGateway gateway;

    public PushNotifier(PushGateway gateway) {
        this.gateway = gateway;
    }

    @Override
    public void deliver(User user, String text) {
        if (user.deviceToken() == null) {
            throw new IllegalStateException("user " + user.id() + " chose the app but has no device");
        }
        gateway.send(user.deviceToken(), text);
    }
}

package alerts;

/** Delivers an alert to a user's phone, or by the fallback when there is no phone. */
public final class SmsNotifier implements Notifier {
    private final SmsGateway gateway;
    private final Notifier fallback;

    public SmsNotifier(SmsGateway gateway, Notifier fallback) {
        this.gateway = gateway;
        this.fallback = fallback;
    }

    @Override
    public void deliver(User user, String text) {
        if (user.phone() == null) {
            fallback.deliver(user, text);
            return;
        }
        gateway.send(user.phone(), text);
    }
}

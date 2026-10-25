package alerts;

/** Delivers an alert to a user's phone. */
public final class SmsNotifier implements Notifier {
    private final SmsGateway gateway;

    public SmsNotifier(SmsGateway gateway) {
        this.gateway = gateway;
    }

    @Override
    public void deliver(User user, String text) {
        if (user.phone() == null) {
            throw new IllegalStateException("user " + user.id() + " chose text messages but has no phone");
        }
        gateway.send(user.phone(), text);
    }
}

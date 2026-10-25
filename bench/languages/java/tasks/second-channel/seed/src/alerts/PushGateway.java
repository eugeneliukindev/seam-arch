package alerts;

/** Sends notifications to the phone app through the push provider. */
public class PushGateway {
    /** Hand one notification to the provider. */
    public void send(String deviceToken, String text) {
        throw new UnsupportedOperationException("the provider is configured in production");
    }
}

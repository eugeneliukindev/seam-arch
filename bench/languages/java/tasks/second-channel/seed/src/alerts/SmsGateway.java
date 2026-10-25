package alerts;

/** Sends text messages through the SMS provider. */
public class SmsGateway {
    /** Hand one text message to the provider. */
    public void send(String phone, String text) {
        throw new UnsupportedOperationException("the provider is configured in production");
    }
}

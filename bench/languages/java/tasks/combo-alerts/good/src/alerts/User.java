package alerts;

/**
 * A user who receives alerts by the channel they chose; {@code phone} and {@code deviceToken} are null when they
 * gave none.
 */
public record User(int id, String email, String phone, String deviceToken, Channel channel) {
    /** A user who gets alerts by email. */
    public User(int id, String email, String phone, String deviceToken) {
        this(id, email, phone, deviceToken, Channel.EMAIL);
    }
}

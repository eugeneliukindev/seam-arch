package alerts;

/** A user who receives alerts by the channel they chose; {@code phone} is null when they gave none. */
public record User(int id, String email, String phone, Channel channel) {
    /** A user who gets alerts by email. */
    public User(int id, String email, String phone) {
        this(id, email, phone, Channel.EMAIL);
    }
}

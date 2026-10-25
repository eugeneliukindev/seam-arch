package alerts;

/** A user who receives alerts; {@code phone} and {@code deviceToken} are null when they gave none. */
public record User(int id, String email, String phone, String deviceToken) {
}

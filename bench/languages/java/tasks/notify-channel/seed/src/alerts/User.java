package alerts;

/** A user who receives alerts; {@code phone} is null when they gave none. */
public record User(int id, String email, String phone) {
}

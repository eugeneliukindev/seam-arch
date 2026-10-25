package accounts;

/** Someone with an account; {@code passwordHash} is empty until a password is set. */
public record User(String email, byte[] passwordHash) {
    public User(String email) {
        this(email, new byte[0]);
    }
}

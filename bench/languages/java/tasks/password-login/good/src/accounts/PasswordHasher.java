package accounts;

/** Turns a password into a stored hash and checks one against it. */
public interface PasswordHasher {
    /** A new hash of {@code password}, different each call. */
    byte[] hash(String password);

    /** Whether {@code password} produced {@code stored}. */
    boolean verify(String password, byte[] stored);
}

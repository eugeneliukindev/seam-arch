package accounts;

import java.security.GeneralSecurityException;
import java.security.MessageDigest;
import java.security.SecureRandom;
import java.util.Arrays;
import java.util.Optional;
import javax.crypto.SecretKeyFactory;
import javax.crypto.spec.PBEKeySpec;

/** Finds and creates accounts. */
public final class AccountService {
    private static final int SALT_SIZE = 16;
    private final SecureRandom random = new SecureRandom();
    private final UserStore users;

    public AccountService(UserStore users) {
        this.users = users;
    }

    /** The account with this email, if there is one. */
    public Optional<User> find(String email) {
        return users.find(email);
    }

    /** Create an account that logs in with {@code password}. */
    public void register(String email, String password) {
        byte[] salt = new byte[SALT_SIZE];
        random.nextBytes(salt);
        byte[] digest = digest(password, salt);
        byte[] stored = Arrays.copyOf(salt, SALT_SIZE + digest.length);
        System.arraycopy(digest, 0, stored, SALT_SIZE, digest.length);
        users.save(new User(email, stored));
    }

    /** Whether {@code password} is the one this account was created with. */
    public boolean logIn(String email, String password) {
        return users.find(email).map(user -> {
            byte[] stored = user.passwordHash();
            byte[] salt = Arrays.copyOfRange(stored, 0, SALT_SIZE);
            return MessageDigest.isEqual(digest(password, salt), Arrays.copyOfRange(stored, SALT_SIZE, stored.length));
        }).orElse(false);
    }

    private static byte[] digest(String password, byte[] salt) {
        try {
            PBEKeySpec spec = new PBEKeySpec(password.toCharArray(), salt, 600_000, 256);
            return SecretKeyFactory.getInstance("PBKDF2WithHmacSHA256").generateSecret(spec).getEncoded();
        } catch (GeneralSecurityException error) {
            throw new IllegalStateException("PBKDF2 is not available", error);
        }
    }
}

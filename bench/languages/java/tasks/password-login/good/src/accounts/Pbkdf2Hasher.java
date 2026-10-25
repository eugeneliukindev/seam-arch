package accounts;

import java.security.GeneralSecurityException;
import java.security.MessageDigest;
import java.security.SecureRandom;
import java.util.Arrays;
import javax.crypto.SecretKeyFactory;
import javax.crypto.spec.PBEKeySpec;

/** Salted PBKDF2 with HMAC-SHA256; the salt is stored in front of the digest. */
public final class Pbkdf2Hasher implements PasswordHasher {
    private final SecureRandom random = new SecureRandom();
    private final int iterations;
    private final int saltSize;
    private final int keyBits;

    public Pbkdf2Hasher(int iterations, int saltSize, int keyBits) {
        this.iterations = iterations;
        this.saltSize = saltSize;
        this.keyBits = keyBits;
    }

    public Pbkdf2Hasher() {
        this(600_000, 16, 256);
    }

    @Override
    public byte[] hash(String password) {
        byte[] salt = new byte[saltSize];
        random.nextBytes(salt);
        byte[] digest = digest(password, salt);
        byte[] stored = Arrays.copyOf(salt, saltSize + digest.length);
        System.arraycopy(digest, 0, stored, saltSize, digest.length);
        return stored;
    }

    @Override
    public boolean verify(String password, byte[] stored) {
        if (stored.length <= saltSize) {
            return false;
        }
        byte[] salt = Arrays.copyOfRange(stored, 0, saltSize);
        return MessageDigest.isEqual(digest(password, salt), Arrays.copyOfRange(stored, saltSize, stored.length));
    }

    private byte[] digest(String password, byte[] salt) {
        PBEKeySpec spec = new PBEKeySpec(password.toCharArray(), salt, iterations, keyBits);
        try {
            return SecretKeyFactory.getInstance("PBKDF2WithHmacSHA256").generateSecret(spec).getEncoded();
        } catch (GeneralSecurityException error) {
            throw new IllegalStateException("PBKDF2 is not available", error);
        } finally {
            spec.clearPassword();
        }
    }
}

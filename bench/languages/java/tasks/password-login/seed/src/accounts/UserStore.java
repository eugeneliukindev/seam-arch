package accounts;

import java.util.Optional;

/** Where users are kept. */
public interface UserStore {
    /** The user with this email, if there is one. */
    Optional<User> find(String email);

    /** Store {@code user}, replacing one with the same email. */
    void save(User user);
}

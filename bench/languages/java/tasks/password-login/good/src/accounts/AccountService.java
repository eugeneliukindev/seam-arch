package accounts;

import java.util.Optional;

/** Finds and creates accounts. */
public final class AccountService {
    private final UserStore users;
    private final PasswordHasher hasher;

    public AccountService(UserStore users, PasswordHasher hasher) {
        this.users = users;
        this.hasher = hasher;
    }

    /** The account with this email, if there is one. */
    public Optional<User> find(String email) {
        return users.find(email);
    }

    /** Create an account that logs in with {@code password}. */
    public void register(String email, String password) {
        users.save(new User(email, hasher.hash(password)));
    }

    /** Whether {@code password} is the one this account was created with. */
    public boolean logIn(String email, String password) {
        return users.find(email).map(user -> hasher.verify(password, user.passwordHash())).orElse(false);
    }
}

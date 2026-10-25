package accounts;

import java.util.Optional;

/** Finds and creates accounts. */
public final class AccountService {
    private final UserStore users;

    public AccountService(UserStore users) {
        this.users = users;
    }

    /** The account with this email, if there is one. */
    public Optional<User> find(String email) {
        return users.find(email);
    }
}

package accounts;

import java.util.HashMap;
import java.util.Map;
import java.util.Optional;

/** Users kept in a map, for one process. */
public final class InMemoryUsers implements UserStore {
    private final Map<String, User> users = new HashMap<>();

    @Override
    public Optional<User> find(String email) {
        return Optional.ofNullable(users.get(email));
    }

    @Override
    public void save(User user) {
        users.put(user.email(), user);
    }
}

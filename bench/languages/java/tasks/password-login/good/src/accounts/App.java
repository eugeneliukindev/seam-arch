package accounts;

/** Builds the account service. */
public final class App {
    private App() {
    }

    /** A ready service with its own store. */
    public static AccountService buildService() {
        return new AccountService(new InMemoryUsers(), new Pbkdf2Hasher());
    }
}

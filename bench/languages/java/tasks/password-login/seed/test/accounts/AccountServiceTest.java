package accounts;

final class AccountServiceTest {
    public static void main(String[] args) {
        check(App.buildService().find("nobody@example.com").isEmpty(), "unknown email has no account");
        System.out.println("AccountServiceTest: ok");
    }

    private static void check(boolean passed, String name) {
        if (!passed) {
            throw new AssertionError(name);
        }
    }
}

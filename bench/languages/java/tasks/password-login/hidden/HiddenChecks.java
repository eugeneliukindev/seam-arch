import accounts.App;

public final class HiddenChecks {
    public static void main(String[] args) throws Exception {
        var service = App.buildService();
        service.register("a@example.com", "s3cret");
        switch (args[0]) {
            case "right" -> expect(service.logIn("a@example.com", "s3cret"), "the right password does not log in");
            case "wrong" -> {
                expect(!service.logIn("a@example.com", "guess"), "a wrong password logs in");
                expect(!service.logIn("b@example.com", "s3cret"), "an unknown email logs in");
            }
            default -> throw new IllegalArgumentException(args[0]);
        }
    }

    private static void expect(boolean passed, String message) {
        if (!passed) {
            throw new AssertionError(message);
        }
    }
}

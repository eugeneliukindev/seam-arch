package alerts;

import java.util.ArrayList;
import java.util.List;

final class AlertServiceTest {
    public static void main(String[] args) {
        List<String> sent = new ArrayList<>();
        SmtpClient smtp = new SmtpClient() {
            @Override
            public void sendMail(String to, String subject, String body) {
                sent.add(to + ": " + body);
            }
        };
        App.buildService(smtp, new SmsGateway(), new PushGateway())
            .alert(new User(1, "a@example.com", null, null), "disk full");
        check(sent.equals(List.of("a@example.com: disk full")), "alert by mail");
        System.out.println("AlertServiceTest: ok");
    }

    private static void check(boolean passed, String name) {
        if (!passed) {
            throw new AssertionError(name);
        }
    }
}

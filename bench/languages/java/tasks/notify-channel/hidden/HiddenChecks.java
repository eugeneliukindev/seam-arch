import alerts.App;
import alerts.Channel;
import alerts.SmsGateway;
import alerts.SmtpClient;
import alerts.User;
import java.util.ArrayList;
import java.util.List;

public final class HiddenChecks {
    public static void main(String[] args) {
        List<String> mails = new ArrayList<>();
        List<String> texts = new ArrayList<>();
        SmtpClient smtp = new SmtpClient() {
            @Override
            public void sendMail(String to, String subject, String body) {
                mails.add(to);
            }
        };
        SmsGateway sms = new SmsGateway() {
            @Override
            public void send(String phone, String text) {
                texts.add(phone);
            }
        };
        var service = App.buildService(smtp, sms);
        switch (args[0]) {
            case "sms" -> {
                service.alert(new User(1, "a@example.com", "+100", Channel.SMS), "disk full");
                expect(texts.equals(List.of("+100")) && mails.isEmpty(), "texts " + texts + ", mails " + mails);
            }
            case "email" -> {
                service.alert(new User(2, "b@example.com", "+200", Channel.EMAIL), "disk full");
                expect(mails.equals(List.of("b@example.com")) && texts.isEmpty(), "texts " + texts + ", mails " + mails);
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

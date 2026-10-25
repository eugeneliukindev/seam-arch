import alerts.App;
import alerts.Channel;
import alerts.PushGateway;
import alerts.SmsGateway;
import alerts.SmtpClient;
import alerts.User;
import java.util.ArrayList;
import java.util.List;

public final class HiddenChecks {
    public static void main(String[] args) {
        switch (args[0]) {
            case "each" -> {
                List<Channel> channels = List.of(Channel.EMAIL, Channel.SMS, Channel.PUSH);
                for (int pick = 0; pick < channels.size(); pick++) {
                    Sinks sinks = new Sinks();
                    sinks.service().alert(new User(1, "a@example.com", "+100", "dev-1", channels.get(pick)), "disk full");
                    List<Integer> expected = new ArrayList<>();
                    for (int i = 0; i < channels.size(); i++) {
                        expected.add(i == pick ? 1 : 0);
                    }
                    expect(sinks.counts().equals(expected), channels.get(pick) + ": sent " + sinks.counts());
                }
            }
            case "fallback" -> {
                Sinks sinks = new Sinks();
                sinks.service().alert(new User(3, "c@example.com", null, null, Channel.SMS), "disk full");
                expect(sinks.mails.equals(List.of("c@example.com")), "mails " + sinks.mails + ", texts " + sinks.texts);
            }
            default -> throw new IllegalArgumentException(args[0]);
        }
    }

    /** Gateways that record where they sent, and the service built on them. */
    private static final class Sinks {
        final List<String> mails = new ArrayList<>();
        final List<String> texts = new ArrayList<>();
        final List<String> pushes = new ArrayList<>();

        alerts.AlertService service() {
            return App.buildService(
                new SmtpClient() {
                    @Override
                    public void sendMail(String to, String subject, String body) {
                        mails.add(to);
                    }
                },
                new SmsGateway() {
                    @Override
                    public void send(String phone, String text) {
                        texts.add(phone);
                    }
                },
                new PushGateway() {
                    @Override
                    public void send(String deviceToken, String text) {
                        pushes.add(deviceToken);
                    }
                });
        }

        List<Integer> counts() {
            return List.of(mails.size(), texts.size(), pushes.size());
        }
    }

    private static void expect(boolean passed, String message) {
        if (!passed) {
            throw new AssertionError(message);
        }
    }
}

import java.util.List;
import java.util.Map;
import weather.Advice;
import weather.ForecastApi;

public final class HiddenChecks {
    public static void main(String[] args) {
        switch (args[0]) {
            case "rain" -> expect(Advice.shouldTakeUmbrella("Oslo", answering(0.7)), "no umbrella at 70% rain");
            case "dry" -> expect(!Advice.shouldTakeUmbrella("Oslo", answering(0.2)), "an umbrella at 20% rain");
            default -> throw new IllegalArgumentException(args[0]);
        }
    }

    /** The provider answering with a fixed payload. */
    private static ForecastApi answering(double rainChance) {
        Map<String, Object> payload = Map.of(
            "daily", List.of(Map.of("pop", rainChance, "tmax", 12.3), Map.of("pop", 0.0, "tmax", 15.0)));
        return new ForecastApi() {
            @Override
            public Map<String, Object> fetch(String city) {
                return payload;
            }
        };
    }

    private static void expect(boolean passed, String message) {
        if (!passed) {
            throw new AssertionError(message);
        }
    }
}

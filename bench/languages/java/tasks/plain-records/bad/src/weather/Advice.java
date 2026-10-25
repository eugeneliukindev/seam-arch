package weather;

import java.util.List;
import java.util.Map;

/** What to wear and carry, from the forecast. */
public final class Advice {
    private static final double RAIN_THRESHOLD = 0.5;

    private Advice() {
    }

    /** Whether rain is more likely than not in {@code city} today. */
    public static boolean shouldTakeUmbrella(String city, ForecastApi api) {
        List<?> daily = (List<?>) api.fetch(city).get("daily");
        Map<?, ?> today = (Map<?, ?>) daily.get(0);
        return ((Number) today.get("pop")).doubleValue() > RAIN_THRESHOLD;
    }
}

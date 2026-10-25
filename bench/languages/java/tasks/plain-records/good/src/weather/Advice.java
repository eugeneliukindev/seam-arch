package weather;

/** What to wear and carry, from the forecast. */
public final class Advice {
    private static final double RAIN_THRESHOLD = 0.5;

    private Advice() {
    }

    /** Whether rain is more likely than not in {@code city} today. */
    public static boolean shouldTakeUmbrella(String city, ForecastApi api) {
        return api.today(city).rainChance() > RAIN_THRESHOLD;
    }
}

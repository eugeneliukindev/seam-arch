package weather;

import java.util.List;
import java.util.Map;

/** Talks to the forecast provider over the network. */
public class ForecastApi {
    private final String baseUrl;

    public ForecastApi() {
        this("https://forecast.example.com");
    }

    public ForecastApi(String baseUrl) {
        this.baseUrl = baseUrl;
    }

    /**
     * The provider's raw JSON for {@code city}, today first, as the JSON parser hands it over.
     *
     * <p>For example {@code {"daily": [{"pop": 0.7, "tmax": 12.3}, {"pop": 0.1, "tmax": 15.0}]}}: a map whose
     * {@code "daily"} entry is a list of maps, where {@code "pop"} is the probability of precipitation from 0 to 1 and
     * {@code "tmax"} the day's highest temperature in degrees Celsius, both as {@code Double}.
     */
    public Map<String, Object> fetch(String city) {
        throw new UnsupportedOperationException("the provider at " + baseUrl + " is configured in production");
    }

    /** Today's forecast for {@code city}. */
    public Forecast today(String city) {
        List<?> daily = (List<?>) fetch(city).get("daily");
        Map<?, ?> today = (Map<?, ?>) daily.get(0);
        return new Forecast(((Number) today.get("pop")).doubleValue());
    }
}

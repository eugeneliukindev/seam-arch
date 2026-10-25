using System.Text.Json.Nodes;

namespace Weather;

/// <summary>Talks to the forecast provider over the network.</summary>
public class ForecastApi(string baseUrl = "https://forecast.example.com")
{
    /// <summary>Where the provider answers.</summary>
    public string BaseUrl { get; } = baseUrl;

    /// <summary>
    /// The provider's raw JSON for <paramref name="city"/>, today first.
    /// For example <c>{"daily": [{"pop": 0.7, "tmax": 12.3}, {"pop": 0.1, "tmax": 15.0}]}</c>,
    /// where <c>pop</c> is the probability of precipitation from 0 to 1 and <c>tmax</c> the
    /// day's highest temperature in degrees Celsius.
    /// </summary>
    public virtual JsonNode Fetch(string city) =>
        throw new NotImplementedException("the provider is configured in production");

    /// <summary>Today's forecast for <paramref name="city"/>.</summary>
    public Forecast Today(string city) => new(Fetch(city)["daily"]![0]!["pop"]!.GetValue<double>());
}

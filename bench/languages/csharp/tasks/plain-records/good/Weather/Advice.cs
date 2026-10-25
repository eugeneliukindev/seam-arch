namespace Weather;

/// <summary>What to wear and carry, from the forecast.</summary>
public static class Advice
{
    private const double RainThreshold = 0.5;

    /// <summary>Whether rain is more likely than not in <paramref name="city"/> today.</summary>
    public static bool ShouldTakeUmbrella(string city, ForecastApi api) => api.Today(city).RainChance > RainThreshold;
}

namespace Weather;

/// <summary>Today's weather in one city; <see cref="RainChance"/> runs from 0 to 1.</summary>
public sealed record Forecast(double RainChance);

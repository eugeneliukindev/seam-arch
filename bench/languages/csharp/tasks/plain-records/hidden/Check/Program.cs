using System.Text.Json.Nodes;
using Weather;

// Hidden checks: one PASS or FAIL line per scenario, read by test_hidden.py.
static void Check(string scenario, Func<bool> passes)
{
    try
    {
        Console.WriteLine($"{(passes() ? "PASS" : "FAIL")} {scenario}");
    }
    catch (Exception error)
    {
        Console.WriteLine($"FAIL {scenario}: {error.GetType().Name}: {error.Message}");
    }
}

Check("likely rain takes an umbrella", () => Advice.ShouldTakeUmbrella("Oslo", new FakeApi(0.7)));
Check("unlikely rain leaves it", () => !Advice.ShouldTakeUmbrella("Oslo", new FakeApi(0.2)));

/// <summary>The provider answering with a fixed payload.</summary>
sealed class FakeApi(double rainChance) : ForecastApi
{
    public override JsonNode Fetch(string city) =>
        JsonNode.Parse($$"""{"daily": [{"pop": {{rainChance.ToString(System.Globalization.CultureInfo.InvariantCulture)}}, "tmax": 12.3}, {"pop": 0.0, "tmax": 15.0}]}""")!;
}

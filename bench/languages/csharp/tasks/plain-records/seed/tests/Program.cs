using Weather;

var failures = 0;

void Check(string test, bool passed)
{
    Console.WriteLine($"{(passed ? "ok  " : "FAIL")} {test}");
    failures += passed ? 0 : 1;
}

bool NeedsTheProvider()
{
    try
    {
        new ForecastApi().Fetch("Oslo");
        return false;
    }
    catch (NotImplementedException)
    {
        return true;
    }
}

Check("fetch needs the provider", NeedsTheProvider());

return failures == 0 ? 0 : 1;

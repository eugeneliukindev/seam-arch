using Resumes;

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

Check("summary of a file", () =>
{
    var resume = Path.Combine(Path.GetTempPath(), $"cv-{Guid.NewGuid()}.txt");
    File.WriteAllText(resume, "Senior Python developer");
    var summary = App.BuildService().Summarize(resume);
    return summary.Grade == "senior" && summary.Words == 3;
});

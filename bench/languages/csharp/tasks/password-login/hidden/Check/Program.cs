using Accounts;

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

Check("right password logs in", () =>
{
    var service = App.BuildService();
    service.Register("a@example.com", "s3cret");
    return service.LogIn("a@example.com", "s3cret");
});
Check("wrong password or email fails", () =>
{
    var service = App.BuildService();
    service.Register("a@example.com", "s3cret");
    return !service.LogIn("a@example.com", "guess") && !service.LogIn("b@example.com", "s3cret");
});

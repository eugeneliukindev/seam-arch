using Accounts;

var failures = 0;

void Check(string test, bool passed)
{
    Console.WriteLine($"{(passed ? "ok  " : "FAIL")} {test}");
    failures += passed ? 0 : 1;
}

Check("unknown email has no account", App.BuildService().Find("nobody@example.com") is null);

return failures == 0 ? 0 : 1;

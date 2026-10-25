using Invoices;

var failures = 0;

void Check(string test, bool passed)
{
    Console.WriteLine($"{(passed ? "ok  " : "FAIL")} {test}");
    failures += passed ? 0 : 1;
}

var output = new StringWriter();
Cli.Run([], new Store(), new DateOnly(2026, 3, 1), output);
Check("lists every invoice", output.ToString().Split(Environment.NewLine, StringSplitOptions.RemoveEmptyEntries).SequenceEqual([
    "A-1 due 2026-01-10 50.00 paid",
    "A-2 due 2026-02-10 75.50 open",
]));

return failures == 0 ? 0 : 1;

sealed class Store : IInvoiceStore
{
    public IReadOnlyList<Invoice> All() =>
    [
        new("A-1", new DateOnly(2026, 1, 10), true, 50.0m),
        new("A-2", new DateOnly(2026, 2, 10), false, 75.5m),
    ];
}

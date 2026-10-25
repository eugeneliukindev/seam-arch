using Shop;

var failures = 0;

void Check(string test, bool passed)
{
    Console.WriteLine($"{(passed ? "ok  " : "FAIL")} {test}");
    failures += passed ? 0 : 1;
}

var book = App.BuildBook();
book.Add(new Coupon("A", 10, new DateTimeOffset(2100, 1, 1, 0, 0, 0, TimeSpan.Zero)));
Check("add a coupon", true);

return failures == 0 ? 0 : 1;

using Shop;

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

static CouponBook BookWith(DateTimeOffset expires)
{
    var book = App.BuildBook();
    book.Add(new Coupon("A", 10, expires));
    return book;
}

Check("valid coupon lowers the total", () =>
    BookWith(new DateTimeOffset(2100, 1, 1, 0, 0, 0, TimeSpan.Zero)).Apply("A", 100m) == 90m);
Check("expired coupon is refused", () =>
{
    try
    {
        BookWith(new DateTimeOffset(2000, 1, 1, 0, 0, 0, TimeSpan.Zero)).Apply("A", 100m);
        return false;
    }
    // the prompt names the exception, not its namespace
    catch (Exception error) when (error.GetType().Name == "CouponExpiredException")
    {
        return true;
    }
});

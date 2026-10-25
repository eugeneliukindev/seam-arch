using System.Reflection;
using System.Text.RegularExpressions;
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

// the prompt names no member for the book, so it is found by its type
static (Checkout Checkout, FakeStripe Stripe) CheckoutWith(DateTimeOffset expires)
{
    var stripe = new FakeStripe();
    var checkout = App.BuildCheckout(stripe);
    var flags = BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic;
    var book = checkout.GetType().GetFields(flags).Select(field => field.GetValue(checkout))
        .Concat(checkout.GetType().GetProperties(flags).Where(p => p.GetIndexParameters().Length == 0).Select(p => p.GetValue(checkout)))
        .OfType<CouponBook>()
        .FirstOrDefault() ?? throw new InvalidOperationException("no coupon book on the checkout");
    book.Add(new Coupon("TEN", 10, expires));
    return (checkout, stripe);
}

Check("valid coupon and GB VAT are charged", () =>
{
    var (checkout, stripe) = CheckoutWith(new DateTimeOffset(2100, 1, 1, 0, 0, 0, TimeSpan.Zero));
    return checkout.Pay(new Cart(100m), "TEN", "GB", "tok") == "ch_1" && stripe.Charges.SequenceEqual([10800]);
});
Check("expired coupon is refused and nothing charged", () =>
{
    var (checkout, stripe) = CheckoutWith(new DateTimeOffset(2000, 1, 1, 0, 0, 0, TimeSpan.Zero));
    try
    {
        checkout.Pay(new Cart(100m), "TEN", "DE", "tok");
        return false;
    }
    catch (Exception error)
    {
        return Regex.IsMatch($"{error.GetType().Name} {error.Message}", "TEN|expir", RegexOptions.IgnoreCase)
            && stripe.Charges.Count == 0;
    }
});

sealed class FakeStripe : StripeClient
{
    public List<int> Charges { get; } = [];

    public override string CreateCharge(int amountCents, string currency, string source)
    {
        Charges.Add(amountCents);
        return "ch_1";
    }
}

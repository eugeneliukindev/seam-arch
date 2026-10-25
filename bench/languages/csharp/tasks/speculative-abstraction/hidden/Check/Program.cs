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

Check("charges in cents", () =>
{
    var stripe = new FakeStripe();
    Payments.Charge(new Order(1, 9.99m, "EUR"), "tok_1", stripe);
    return stripe.Charges.SequenceEqual([(999, "EUR", "tok_1")]);
});

sealed class FakeStripe : StripeClient
{
    public List<(int AmountCents, string Currency, string Source)> Charges { get; } = [];

    // Stripe itself takes the code in lower case; the case is not the point of the task
    public override string CreateCharge(int amountCents, string currency, string source)
    {
        Charges.Add((amountCents, currency.ToUpperInvariant(), source));
        return "ch_1";
    }
}

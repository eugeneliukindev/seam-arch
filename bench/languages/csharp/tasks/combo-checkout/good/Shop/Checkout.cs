namespace Shop;

/// <summary>What the customer is buying, in euros.</summary>
public sealed record Cart(decimal Total);

/// <summary>Discounts, taxes and charges a cart.</summary>
public sealed class Checkout(CouponBook coupons, StripeClient client)
{
    private const int CentsPerEuro = 100;

    private static readonly Dictionary<string, decimal> VatRates = new()
    {
        ["GB"] = 0.20m,
        ["DE"] = 0.19m,
        ["NL"] = 0.21m,
    };

    /// <summary>Charge the cart after its coupon and VAT and return the charge id.</summary>
    public string Pay(Cart cart, string code, string country, string cardToken)
    {
        var net = coupons.Discounted(code, cart.Total);
        var gross = net * (1 + VatRates.GetValueOrDefault(country));
        return client.CreateCharge((int)Math.Round(gross * CentsPerEuro), "EUR", cardToken);
    }
}

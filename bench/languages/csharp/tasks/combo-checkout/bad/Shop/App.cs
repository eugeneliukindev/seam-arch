namespace Shop;

/// <summary>Builds the checkout the site uses.</summary>
public static class App
{
    /// <summary>A checkout with an empty coupon book, charging through <paramref name="client"/>.</summary>
    public static Checkout BuildCheckout(StripeClient client) => new(new CouponBook(), client);
}

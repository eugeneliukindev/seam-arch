namespace Shop;

/// <summary>A discount a customer can redeem until <see cref="Expires"/>, a moment in UTC.</summary>
public sealed record Coupon(string Code, int Percent, DateTimeOffset Expires);

/// <summary>The coupons the shop has issued.</summary>
public sealed class CouponBook
{
    private readonly Dictionary<string, Coupon> _coupons = [];

    /// <summary>Issue <paramref name="coupon"/>.</summary>
    public void Add(Coupon coupon) => _coupons[coupon.Code] = coupon;
}

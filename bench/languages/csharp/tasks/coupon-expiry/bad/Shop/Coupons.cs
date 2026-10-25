namespace Shop;

/// <summary>The coupon's expiry moment has passed.</summary>
public sealed class CouponExpiredException(string code) : Exception($"coupon {code} has expired");

/// <summary>A discount a customer can redeem until <see cref="Expires"/>, a moment in UTC.</summary>
public sealed record Coupon(string Code, int Percent, DateTimeOffset Expires);

/// <summary>The coupons the shop has issued.</summary>
public sealed class CouponBook
{
    private readonly Dictionary<string, Coupon> _coupons = [];

    /// <summary>Issue <paramref name="coupon"/>.</summary>
    public void Add(Coupon coupon) => _coupons[coupon.Code] = coupon;

    /// <summary><paramref name="total"/> lowered by the coupon's percent; <see cref="CouponExpiredException"/> once it has expired.</summary>
    public decimal Apply(string code, decimal total)
    {
        var coupon = _coupons[code];
        if (DateTimeOffset.UtcNow >= coupon.Expires)
        {
            throw new CouponExpiredException(code);
        }
        return total * (100 - coupon.Percent) / 100;
    }
}

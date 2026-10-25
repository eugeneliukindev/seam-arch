namespace Shop;

/// <summary>The client the Stripe SDK would give us; kept small here.</summary>
public class StripeClient
{
    /// <summary>Charge <paramref name="source"/> and return the charge id.</summary>
    public virtual string CreateCharge(int amountCents, string currency, string source) =>
        throw new NotImplementedException("configured in production");
}

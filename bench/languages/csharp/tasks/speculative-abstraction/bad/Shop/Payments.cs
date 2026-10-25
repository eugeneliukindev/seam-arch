namespace Shop;

/// <summary>Takes payments for orders.</summary>
public interface IPaymentGateway
{
    string Charge(Order order, string cardToken);
}

/// <summary>Paying for orders.</summary>
public static class Payments
{
    private const int CentsPerUnit = 100;

    /// <summary>Charge <paramref name="order"/> to the card behind <paramref name="cardToken"/> and return the charge id.</summary>
    public static string Charge(Order order, string cardToken, StripeClient client) =>
        client.CreateCharge(amountCents: (int)(order.Total * CentsPerUnit), currency: order.Currency, source: cardToken);
}

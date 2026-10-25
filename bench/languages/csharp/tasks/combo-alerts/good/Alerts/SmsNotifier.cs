namespace Alerts;

/// <summary>Delivers an alert to a user's phone, or by <paramref name="fallback"/> when there is no phone.</summary>
public sealed class SmsNotifier(SmsGateway gateway, INotifier fallback) : INotifier
{
    /// <summary>Text <paramref name="text"/> to <paramref name="user"/>.</summary>
    public void Notify(User user, string text)
    {
        if (user.Phone is null)
        {
            fallback.Notify(user, text);
            return;
        }
        gateway.Send(user.Phone, text);
    }
}

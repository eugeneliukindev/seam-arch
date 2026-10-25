namespace Alerts;

/// <summary>Delivers an alert to a user's phone.</summary>
public sealed class SmsNotifier(SmsGateway gateway) : INotifier
{
    /// <summary>Text <paramref name="text"/> to <paramref name="user"/>.</summary>
    public void Notify(User user, string text) =>
        gateway.Send(user.Phone ?? throw new InvalidOperationException($"user {user.Id} chose text messages but has no phone"), text);
}

namespace Alerts;

/// <summary>Delivers an alert to a user's phone app.</summary>
public sealed class PushNotifier(PushGateway gateway) : INotifier
{
    /// <summary>Push <paramref name="text"/> to <paramref name="user"/>'s app.</summary>
    public void Notify(User user, string text) =>
        gateway.Send(user.DeviceToken ?? throw new InvalidOperationException($"user {user.Id} chose push but has no device"), text);
}

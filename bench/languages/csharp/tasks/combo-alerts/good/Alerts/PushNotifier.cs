namespace Alerts;

/// <summary>Delivers an alert to a user's phone app, or by <paramref name="fallback"/> when there is no device.</summary>
public sealed class PushNotifier(PushGateway gateway, INotifier fallback) : INotifier
{
    /// <summary>Push <paramref name="text"/> to <paramref name="user"/>'s app.</summary>
    public void Notify(User user, string text)
    {
        if (user.DeviceToken is null)
        {
            fallback.Notify(user, text);
            return;
        }
        gateway.Send(user.DeviceToken, text);
    }
}

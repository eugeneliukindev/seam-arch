namespace Alerts;

/// <summary>Raises alerts for users, each by the channel they chose.</summary>
public sealed class AlertService(IReadOnlyDictionary<Channel, INotifier> notifiers)
{
    /// <summary>Deliver <paramref name="text"/> to <paramref name="user"/>.</summary>
    public void Alert(User user, string text) => notifiers[user.Channel].Notify(user, text);
}

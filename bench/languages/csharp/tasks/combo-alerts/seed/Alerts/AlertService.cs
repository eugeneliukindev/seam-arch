namespace Alerts;

/// <summary>Raises alerts for users.</summary>
public sealed class AlertService(EmailNotifier notifier)
{
    /// <summary>Deliver <paramref name="text"/> to <paramref name="user"/>.</summary>
    public void Alert(User user, string text) => notifier.Notify(user, text);
}

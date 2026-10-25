namespace Alerts;

/// <summary>Delivers an alert by one channel.</summary>
public interface INotifier
{
    /// <summary>Deliver <paramref name="text"/> to <paramref name="user"/>.</summary>
    void Notify(User user, string text);
}

namespace Alerts;

/// <summary>Raises alerts for users.</summary>
public sealed class AlertService(EmailNotifier notifier, SmsGateway sms, PushGateway push)
{
    /// <summary>Deliver <paramref name="text"/> to <paramref name="user"/>.</summary>
    public void Alert(User user, string text)
    {
        if (user.Channel == Channel.Sms && user.Phone is not null)
        {
            sms.Send(user.Phone, text);
        }
        else if (user.Channel == Channel.Push && user.DeviceToken is not null)
        {
            push.Send(user.DeviceToken, text);
        }
        else
        {
            notifier.Notify(user, text);
        }
    }
}

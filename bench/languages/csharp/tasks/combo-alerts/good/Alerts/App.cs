namespace Alerts;

/// <summary>Builds the alert service from the delivery clients.</summary>
public static class App
{
    /// <summary>The alert service the application uses.</summary>
    public static AlertService BuildService(SmtpClient smtp, SmsGateway sms, PushGateway push)
    {
        var email = new EmailNotifier(smtp);
        return new(new Dictionary<Channel, INotifier>
        {
            [Channel.Email] = email,
            [Channel.Sms] = new SmsNotifier(sms, fallback: email),
            [Channel.Push] = new PushNotifier(push, fallback: email),
        });
    }
}

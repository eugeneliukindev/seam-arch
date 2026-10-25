namespace Alerts;

/// <summary>Builds the alert service from the delivery clients.</summary>
public static class App
{
    /// <summary>The alert service the application uses.</summary>
    public static AlertService BuildService(SmtpClient smtp, SmsGateway sms) => new(new EmailNotifier(smtp), sms);
}

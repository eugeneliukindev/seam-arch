namespace Alerts;

/// <summary>Sends mail through the mail relay.</summary>
public class SmtpClient
{
    /// <summary>Hand one message to the relay.</summary>
    public virtual void SendMail(string to, string subject, string body) =>
        throw new NotImplementedException("the relay is configured in production");
}

/// <summary>Sends text messages through the SMS provider.</summary>
public class SmsGateway
{
    /// <summary>Hand one text message to the provider.</summary>
    public virtual void Send(string phone, string text) =>
        throw new NotImplementedException("the provider is configured in production");
}

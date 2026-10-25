namespace Alerts;

/// <summary>Delivers an alert to a user's mailbox.</summary>
public sealed class EmailNotifier(SmtpClient smtp)
{
    /// <summary>Mail <paramref name="text"/> to <paramref name="user"/>.</summary>
    public void Notify(User user, string text) => smtp.SendMail(user.Email, subject: "Alert", body: text);
}

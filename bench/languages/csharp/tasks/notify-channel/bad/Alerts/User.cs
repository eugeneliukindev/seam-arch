namespace Alerts;

/// <summary>How a user chose to receive alerts.</summary>
public enum Channel
{
    Email,
    Sms,
}

/// <summary>A user who receives alerts, by the channel they chose.</summary>
public sealed record User(int Id, string Email, string? Phone = null, Channel Channel = Channel.Email);

namespace Alerts;

/// <summary>A user who receives alerts.</summary>
public sealed record User(int Id, string Email, string? Phone = null);

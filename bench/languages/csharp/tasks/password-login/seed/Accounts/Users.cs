namespace Accounts;

/// <summary>Someone with an account.</summary>
public sealed record User(string Email)
{
    public byte[] PasswordHash { get; init; } = [];
}

/// <summary>Where users are kept.</summary>
public interface IUserStore
{
    /// <summary>The user with this email, or <c>null</c>.</summary>
    User? Find(string email);

    /// <summary>Store <paramref name="user"/>, replacing one with the same email.</summary>
    void Save(User user);
}

/// <summary>Users kept in a dictionary, for one process.</summary>
public sealed class InMemoryUsers : IUserStore
{
    private readonly Dictionary<string, User> _users = [];

    public User? Find(string email) => _users.GetValueOrDefault(email);

    public void Save(User user) => _users[user.Email] = user;
}

namespace Accounts;

/// <summary>Finds and creates accounts.</summary>
public sealed class AccountService(IUserStore users, IPasswordHasher hasher)
{
    /// <summary>The account with this email, or <c>null</c>.</summary>
    public User? Find(string email) => users.Find(email);

    /// <summary>Create an account that logs in with <paramref name="password"/>.</summary>
    public void Register(string email, string password) =>
        users.Save(new User(email) { PasswordHash = hasher.Hash(password) });

    /// <summary>Whether <paramref name="password"/> is the one this account was created with.</summary>
    public bool LogIn(string email, string password) =>
        users.Find(email) is { } user && hasher.Verify(password, user.PasswordHash);
}

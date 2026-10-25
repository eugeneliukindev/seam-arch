namespace Accounts;

/// <summary>Finds and creates accounts.</summary>
public sealed class AccountService(IUserStore users)
{
    /// <summary>The account with this email, or <c>null</c>.</summary>
    public User? Find(string email) => users.Find(email);
}

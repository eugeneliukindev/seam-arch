using System.Security.Cryptography;

namespace Accounts;

/// <summary>Finds and creates accounts.</summary>
public sealed class AccountService(IUserStore users, int saltSize = 16)
{
    private const int Iterations = 600_000;
    private const int DigestSize = 32;

    /// <summary>The account with this email, or <c>null</c>.</summary>
    public User? Find(string email) => users.Find(email);

    /// <summary>Create an account that logs in with <paramref name="password"/>.</summary>
    public void Register(string email, string password)
    {
        var salt = RandomNumberGenerator.GetBytes(saltSize);
        var digest = Rfc2898DeriveBytes.Pbkdf2(password, salt, Iterations, HashAlgorithmName.SHA256, DigestSize);
        users.Save(new User(email) { PasswordHash = [.. salt, .. digest] });
    }

    /// <summary>Whether <paramref name="password"/> is the one this account was created with.</summary>
    public bool LogIn(string email, string password)
    {
        if (users.Find(email) is not { } user)
        {
            return false;
        }
        var salt = user.PasswordHash[..saltSize];
        var candidate = Rfc2898DeriveBytes.Pbkdf2(password, salt, Iterations, HashAlgorithmName.SHA256, DigestSize);
        return CryptographicOperations.FixedTimeEquals(candidate, user.PasswordHash[saltSize..]);
    }
}

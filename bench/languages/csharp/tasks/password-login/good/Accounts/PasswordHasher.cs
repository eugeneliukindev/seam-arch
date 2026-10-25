using System.Security.Cryptography;

namespace Accounts;

/// <summary>Turns a password into a stored hash and checks one against it.</summary>
public interface IPasswordHasher
{
    /// <summary>A new hash of <paramref name="password"/>, different each call.</summary>
    byte[] Hash(string password);

    /// <summary>Whether <paramref name="password"/> produced <paramref name="stored"/>.</summary>
    bool Verify(string password, byte[] stored);
}

/// <summary>Salted PBKDF2 over SHA-256; the salt is stored in front of the digest.</summary>
public sealed class Pbkdf2PasswordHasher(int iterations = 600_000, int saltSize = 16, int digestSize = 32) : IPasswordHasher
{
    public byte[] Hash(string password)
    {
        var salt = RandomNumberGenerator.GetBytes(saltSize);
        return [.. salt, .. Digest(password, salt)];
    }

    public bool Verify(string password, byte[] stored) =>
        stored.Length == saltSize + digestSize
        && CryptographicOperations.FixedTimeEquals(Digest(password, stored[..saltSize]), stored[saltSize..]);

    private byte[] Digest(string password, byte[] salt) =>
        Rfc2898DeriveBytes.Pbkdf2(password, salt, iterations, HashAlgorithmName.SHA256, digestSize);
}

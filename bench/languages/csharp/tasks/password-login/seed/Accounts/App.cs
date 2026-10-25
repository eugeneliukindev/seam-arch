namespace Accounts;

/// <summary>Builds the account service.</summary>
public static class App
{
    /// <summary>A ready service with its own store.</summary>
    public static AccountService BuildService() => new(new InMemoryUsers());
}

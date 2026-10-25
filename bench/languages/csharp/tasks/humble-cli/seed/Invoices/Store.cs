namespace Invoices;

/// <summary>One invoice sent to a customer.</summary>
public sealed record Invoice(string Number, DateOnly Due, bool Paid, decimal Amount);

/// <summary>Every invoice we have sent.</summary>
public interface IInvoiceStore
{
    /// <summary>All invoices, in the order they were sent.</summary>
    IReadOnlyList<Invoice> All();
}

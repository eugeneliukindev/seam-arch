namespace Invoices;

/// <summary>An unpaid invoice past its due date, by <see cref="Days"/>.</summary>
public sealed record OverdueInvoice(Invoice Invoice, int Days);

/// <summary>Which invoices are overdue, and by how long.</summary>
public static class Overdue
{
    /// <summary>The unpaid invoices due before <paramref name="today"/>, oldest first.</summary>
    public static IReadOnlyList<OverdueInvoice> Of(IEnumerable<Invoice> invoices, DateOnly today) =>
        [.. invoices
            .Where(invoice => !invoice.Paid && invoice.Due < today)
            .OrderBy(invoice => invoice.Due)
            .Select(invoice => new OverdueInvoice(invoice, today.DayNumber - invoice.Due.DayNumber))];
}

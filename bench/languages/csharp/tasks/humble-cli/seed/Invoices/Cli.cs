using static System.FormattableString;

namespace Invoices;

/// <summary>The <c>invoices</c> command.</summary>
public static class Cli
{
    /// <summary>Print the invoices to <paramref name="output"/>, one per line.</summary>
    public static void Run(string[] args, IInvoiceStore store, DateOnly today, TextWriter output)
    {
        foreach (var invoice in store.All())
        {
            var status = invoice.Paid ? "paid" : "open";
            output.WriteLine(Invariant($"{invoice.Number} due {invoice.Due:yyyy-MM-dd} {invoice.Amount:F2} {status}"));
        }
    }
}

package invoices;

import java.io.PrintStream;
import java.time.LocalDate;
import java.util.Locale;

/** The {@code invoices} command. */
public final class Cli {
    private Cli() {
    }

    /** Print the invoices, one per line. */
    public static void run(String[] args, InvoiceStore store, LocalDate today, PrintStream out) {
        if (args.length > 0) {
            throw new IllegalArgumentException("usage: invoices");
        }
        for (Invoice invoice : store.all()) {
            String status = invoice.paid() ? "paid" : "open";
            out.println(String.format(Locale.ROOT, "%s due %s %.2f %s", invoice.number(), invoice.due(), invoice.amount(), status));
        }
    }
}

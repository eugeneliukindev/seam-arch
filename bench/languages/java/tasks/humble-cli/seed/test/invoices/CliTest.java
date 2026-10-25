package invoices;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.math.BigDecimal;
import java.nio.charset.StandardCharsets;
import java.time.LocalDate;
import java.util.List;

final class CliTest {
    public static void main(String[] args) {
        InvoiceStore store = () -> List.of(
            new Invoice("A-1", LocalDate.of(2026, 1, 10), true, new BigDecimal("50.00")),
            new Invoice("A-2", LocalDate.of(2026, 2, 10), false, new BigDecimal("75.50")));
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        Cli.run(new String[0], store, LocalDate.of(2026, 3, 1), new PrintStream(out, true, StandardCharsets.UTF_8));
        List<String> lines = out.toString(StandardCharsets.UTF_8).lines().toList();
        check(lines.equals(List.of("A-1 due 2026-01-10 50.00 paid", "A-2 due 2026-02-10 75.50 open")), "lists every invoice");
        System.out.println("CliTest: ok");
    }

    private static void check(boolean passed, String name) {
        if (!passed) {
            throw new AssertionError(name);
        }
    }
}

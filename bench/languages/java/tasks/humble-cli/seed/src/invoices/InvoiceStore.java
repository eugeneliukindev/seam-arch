package invoices;

import java.util.List;

/** Every invoice we have sent. */
public interface InvoiceStore {
    /** All invoices, in the order they were sent. */
    List<Invoice> all();
}

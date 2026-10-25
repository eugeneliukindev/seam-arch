use invoices::cli::run;
use invoices::date::Date;
use invoices::store::{Invoice, InvoiceStore};

struct Store;

impl InvoiceStore for Store {
    fn all(&self) -> Vec<Invoice> {
        vec![
            Invoice { number: "A-1".into(), due: Date::new(2026, 1, 10), paid: true, amount: 50.0 },
            Invoice { number: "A-2".into(), due: Date::new(2026, 2, 10), paid: false, amount: 75.5 },
        ]
    }
}

#[test]
fn lists_every_invoice() {
    let mut out = Vec::new();
    run(&[], &Store, Date::new(2026, 3, 1), &mut out).unwrap();
    assert_eq!(String::from_utf8(out).unwrap(), "A-1 due 2026-01-10 50.00 paid\nA-2 due 2026-02-10 75.50 open\n");
}

#[test]
fn days_between_dates() {
    assert_eq!(Date::new(2026, 10, 1) - Date::new(2026, 7, 3), 90);
    assert_eq!(Date::new(2024, 3, 1) - Date::new(2024, 2, 28), 2);
}

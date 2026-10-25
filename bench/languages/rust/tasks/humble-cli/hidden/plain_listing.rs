use invoices::cli::run;
use invoices::date::Date;
use invoices::store::{Invoice, InvoiceStore};

struct Store;

impl InvoiceStore for Store {
    fn all(&self) -> Vec<Invoice> {
        let invoice = |number: &str, due: Date, paid: bool, amount: f64| Invoice { number: number.into(), due, paid, amount };
        vec![
            invoice("N-3", Date::new(2026, 9, 21), false, 300.0),
            invoice("N-1", Date::new(2026, 7, 3), false, 120.0),
            invoice("N-2", Date::new(2026, 8, 25), true, 80.0),
            invoice("N-4", Date::new(2026, 10, 1), false, 60.0),
            invoice("N-5", Date::new(2026, 11, 15), false, 90.0),
            invoice("N-6", Date::new(2026, 9, 2), false, 45.25),
        ]
    }
}

const TODAY: (i32, u32, u32) = (2026, 10, 1);

fn printed(args: &[&str]) -> String {
    let mut out = Vec::new();
    run(args, &Store, Date::new(TODAY.0, TODAY.1, TODAY.2), &mut out).unwrap();
    String::from_utf8(out).unwrap()
}

#[test]
fn plain_listing_still_lists_everything() {
    let shown = printed(&[]);
    for number in ["N-1", "N-2", "N-3", "N-4", "N-5", "N-6"] {
        assert!(shown.contains(number), "{number} missing from {shown}");
    }
}

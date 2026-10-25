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

/// The first invoice number on `line`, such as `N-3`.
fn number_in(line: &str) -> Option<String> {
    line.match_indices("N-").find_map(|(start, _)| {
        let digits: String = line[start + 2..].chars().take_while(char::is_ascii_digit).collect();
        (!digits.is_empty()).then(|| format!("N-{digits}"))
    })
}

#[test]
fn overdue_lists_late_invoices_oldest_first() {
    // oldest first, with days overdue
    let expected = [("N-1", 90), ("N-6", 29), ("N-3", 10)];
    let shown = printed(&["--overdue"]);
    let lines: Vec<(String, &str)> = shown.lines().filter_map(|line| number_in(line).map(|number| (number, line))).collect();
    let numbers: Vec<&str> = lines.iter().map(|(number, _)| number.as_str()).collect();
    assert_eq!(numbers, expected.map(|(number, _)| number), "{shown}");
    for ((_, line), (_, days)) in lines.iter().zip(expected) {
        // a number standing on its own: not part of a date, an amount or an invoice number
        let found = line.split(|c: char| !(c.is_ascii_digit() || c == '.' || c == '-')).any(|token| token == days.to_string());
        assert!(found, "no {days} days in {line:?}");
    }
}

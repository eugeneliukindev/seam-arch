//! Which invoices are overdue, and by how long.

use crate::date::Date;
use crate::store::Invoice;

/// An unpaid invoice past its due date.
#[derive(Debug, Clone, PartialEq)]
pub struct Overdue {
    pub invoice: Invoice,
    pub days: i64,
}

/// The unpaid invoices due before `today`, oldest first.
pub fn overdue(invoices: Vec<Invoice>, today: Date) -> Vec<Overdue> {
    let mut late: Vec<Invoice> = invoices.into_iter().filter(|invoice| !invoice.paid && invoice.due < today).collect();
    late.sort_by_key(|invoice| invoice.due);
    late.into_iter().map(|invoice| Overdue { days: today - invoice.due, invoice }).collect()
}

//! Invoices and where they are kept.

use crate::date::Date;

/// One invoice sent to a customer.
#[derive(Debug, Clone, PartialEq)]
pub struct Invoice {
    pub number: String,
    pub due: Date,
    pub paid: bool,
    pub amount: f64,
}

/// Every invoice we have sent.
pub trait InvoiceStore {
    /// All invoices, in the order they were sent.
    fn all(&self) -> Vec<Invoice>;
}

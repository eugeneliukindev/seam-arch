//! Orders customers place.

/// An order waiting for payment.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Order {
    pub id: u64,
    pub total_cents: u64,
    pub currency: String,
}

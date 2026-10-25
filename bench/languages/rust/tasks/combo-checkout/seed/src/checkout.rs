//! Taking the customer's money.

/// What the customer is buying.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Cart {
    pub total_cents: u64,
}

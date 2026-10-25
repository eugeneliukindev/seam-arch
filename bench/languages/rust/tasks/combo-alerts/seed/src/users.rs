//! The people alerts go to.

/// A user who receives alerts.
#[derive(Debug, Clone, Default, PartialEq, Eq)]
pub struct User {
    pub id: u64,
    pub email: String,
    pub phone: Option<String>,
    pub device_token: Option<String>,
}

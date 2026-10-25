//! The people alerts go to.

/// How a user chose to receive alerts.
#[derive(Debug, Clone, Copy, Default, PartialEq, Eq, Hash)]
pub enum Channel {
    #[default]
    Email,
    Sms,
    Push,
}

/// A user who receives alerts, by the channel they chose.
#[derive(Debug, Clone, Default, PartialEq, Eq)]
pub struct User {
    pub id: u64,
    pub email: String,
    pub phone: Option<String>,
    pub device_token: Option<String>,
    pub channel: Channel,
}

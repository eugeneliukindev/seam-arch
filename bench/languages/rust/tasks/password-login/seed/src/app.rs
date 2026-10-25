//! Builds the account service.

use crate::service::AccountService;
use crate::users::InMemoryUsers;

/// A ready service with its own store.
pub fn build_service() -> AccountService {
    AccountService::new(Box::new(InMemoryUsers::default()))
}

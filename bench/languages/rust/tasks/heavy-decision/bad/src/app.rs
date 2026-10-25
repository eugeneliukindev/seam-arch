//! Builds the resume services.

use crate::service::ResumeService;

/// A service reading resumes from disk.
pub fn build_service() -> ResumeService {
    ResumeService
}

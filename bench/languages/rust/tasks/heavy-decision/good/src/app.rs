//! Builds the resume services.

use std::io;
use std::path::Path;

use crate::files::read_text_file;
use crate::service::ResumeService;

/// A service reading resumes from disk.
pub fn build_service() -> ResumeService<fn(&Path) -> io::Result<String>> {
    ResumeService::new(read_text_file)
}

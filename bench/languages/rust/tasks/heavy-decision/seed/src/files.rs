//! Resume files on disk.

use std::fs;
use std::io;
use std::path::Path;

/// The text of a resume file.
pub fn read_text_file(path: &Path) -> io::Result<String> {
    fs::read_to_string(path)
}

//! What a resume says about its author.

use std::fs;
use std::io;
use std::path::Path;

use crate::grading::{grade_of, Grade};

/// A resume in two numbers.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Summary {
    pub grade: Option<Grade>,
    pub words: usize,
}

/// Summarizes resumes from disk.
pub struct ResumeService;

impl ResumeService {
    /// The grade the resume names and its length in words.
    pub fn summarize(&self, path: &Path) -> io::Result<Summary> {
        let text = fs::read_to_string(path)?;
        Ok(Summary { grade: grade_of(&text), words: text.split_whitespace().count() })
    }
}

//! What a resume says about its author.

use std::io;
use std::path::Path;

use crate::grading::{grade_of, Grade};

/// A resume in two numbers.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Summary {
    pub grade: Option<Grade>,
    pub words: usize,
}

/// Summarizes resumes; how a file is read is passed in.
pub struct ResumeService<R> {
    read: R,
}

impl<R: Fn(&Path) -> io::Result<String>> ResumeService<R> {
    pub fn new(read: R) -> Self {
        Self { read }
    }

    /// The grade the resume names and its length in words.
    pub fn summarize(&self, path: &Path) -> io::Result<Summary> {
        let text = (self.read)(path)?;
        Ok(Summary { grade: grade_of(&text), words: text.split_whitespace().count() })
    }
}

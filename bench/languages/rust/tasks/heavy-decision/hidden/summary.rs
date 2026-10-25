use std::fs;

use resumes::app::build_service;
use resumes::grading::Grade;

#[test]
fn summary_of_a_file() {
    let path = std::env::temp_dir().join(format!("resume-{}.txt", std::process::id()));
    fs::write(&path, "Senior Rust developer").unwrap();
    let summary = build_service().summarize(&path);
    fs::remove_file(&path).unwrap();
    let summary = summary.unwrap();
    assert_eq!((summary.grade, summary.words), (Some(Grade::Senior), 3));
}

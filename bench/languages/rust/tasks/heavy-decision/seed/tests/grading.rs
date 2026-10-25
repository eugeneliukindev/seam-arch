use resumes::grading::{grade_of, Grade};

#[test]
fn senior_beats_junior() {
    assert_eq!(grade_of("Senior engineer, mentored juniors"), Some(Grade::Senior));
}

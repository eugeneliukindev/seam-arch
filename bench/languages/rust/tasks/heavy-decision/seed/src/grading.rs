//! How senior a resume reads.

/// How senior the author of a resume is.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Grade {
    Lead,
    Senior,
    Middle,
    Junior,
}

const GRADES: [(Grade, &[&str]); 4] = [
    (Grade::Lead, &["lead", "principal", "head of"]),
    (Grade::Senior, &["senior", "sr"]),
    (Grade::Middle, &["middle", "mid"]),
    (Grade::Junior, &["junior", "jr", "intern"]),
];

/// The highest grade the resume names, or `None`; slow on long resumes, since every rule scans the whole text.
pub fn grade_of(text: &str) -> Option<Grade> {
    let words: Vec<String> = text
        .split(|character: char| !character.is_alphanumeric())
        .filter(|word| !word.is_empty())
        .map(str::to_lowercase)
        .collect();
    let phrase = format!(" {} ", words.join(" "));
    GRADES
        .iter()
        .find(|(_, names)| names.iter().any(|name| phrase.contains(&format!(" {name} "))))
        .map(|(grade, _)| *grade)
}

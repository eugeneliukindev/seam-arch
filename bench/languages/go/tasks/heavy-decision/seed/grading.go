package resumes

import "regexp"

var grades = []struct {
	grade   string
	pattern *regexp.Regexp
}{
	{"lead", regexp.MustCompile(`(?i)\b(?:lead|principal|head\s+of)\b`)},
	{"senior", regexp.MustCompile(`(?i)\b(?:senior|sr\.?)\b`)},
	{"middle", regexp.MustCompile(`(?i)\b(?:middle|mid)\b`)},
	{"junior", regexp.MustCompile(`(?i)\b(?:junior|jr\.?|intern)\b`)},
}

// GradeOf returns the highest grade the resume names, or "" if it names none;
// slow on long resumes, since every rule scans the whole text.
func GradeOf(text string) string {
	for _, rule := range grades {
		if rule.pattern.MatchString(text) {
			return rule.grade
		}
	}
	return ""
}

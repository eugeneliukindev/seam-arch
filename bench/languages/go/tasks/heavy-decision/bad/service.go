package resumes

import (
	"fmt"
	"os"
	"strings"
)

// Summary is a resume in two numbers.
type Summary struct {
	Grade string
	Words int
}

// ResumeService summarizes resumes from disk.
type ResumeService struct{}

// Summarize returns the grade the resume names and its length in words.
func (s *ResumeService) Summarize(path string) (Summary, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return Summary{}, fmt.Errorf("read resume: %w", err)
	}
	text := string(data)
	return Summary{Grade: GradeOf(text), Words: len(strings.Fields(text))}, nil
}

package resumes

import "strings"

// Summary is a resume in two numbers.
type Summary struct {
	Grade string
	Words int
}

// ResumeService summarizes resumes; how a file is read is passed in.
type ResumeService struct {
	read func(path string) (string, error)
}

// NewResumeService returns a service reading files with read.
func NewResumeService(read func(path string) (string, error)) *ResumeService {
	return &ResumeService{read: read}
}

// Summarize returns the grade the resume names and its length in words.
func (s *ResumeService) Summarize(path string) (Summary, error) {
	text, err := s.read(path)
	if err != nil {
		return Summary{}, err
	}
	return Summary{Grade: GradeOf(text), Words: len(strings.Fields(text))}, nil
}

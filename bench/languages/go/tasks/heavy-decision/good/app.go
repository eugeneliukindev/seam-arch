// Package resumes reads resumes.
package resumes

// BuildService returns a service reading resumes from disk.
func BuildService() *ResumeService {
	return NewResumeService(ReadTextFile)
}

package resumes

import (
	"fmt"
	"os"
)

// ReadTextFile returns the text of a resume file.
func ReadTextFile(path string) (string, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return "", fmt.Errorf("read resume: %w", err)
	}
	return string(data), nil
}

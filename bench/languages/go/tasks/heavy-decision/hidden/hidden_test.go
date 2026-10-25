package resumes_test

import (
	"os"
	"path/filepath"
	"testing"

	"example.com/resumes"
)

func TestHiddenSummaryOfAFile(t *testing.T) {
	path := filepath.Join(t.TempDir(), "cv.txt")
	if err := os.WriteFile(path, []byte("Senior Go developer"), 0o600); err != nil {
		t.Fatal(err)
	}
	summary, err := resumes.BuildService().Summarize(path)
	if err != nil || summary.Grade != "senior" || summary.Words != 3 {
		t.Fatalf("Summarize = %+v, %v; want senior, 3 words", summary, err)
	}
}

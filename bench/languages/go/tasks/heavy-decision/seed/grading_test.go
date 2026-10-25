package resumes

import "testing"

func TestSeniorBeatsJunior(t *testing.T) {
	if got := GradeOf("Senior engineer, mentored juniors"); got != "senior" {
		t.Fatalf("GradeOf = %q; want senior", got)
	}
}

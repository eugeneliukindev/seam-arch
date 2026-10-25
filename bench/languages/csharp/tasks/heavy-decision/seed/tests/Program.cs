using Resumes;

var failures = 0;

void Check(string test, bool passed)
{
    Console.WriteLine($"{(passed ? "ok  " : "FAIL")} {test}");
    failures += passed ? 0 : 1;
}

Check("senior beats junior", Grading.GradeOf("Senior engineer, mentored juniors") == "senior");

return failures == 0 ? 0 : 1;

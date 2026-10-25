package resumes;

import java.util.Optional;

final class GradingTest {
    public static void main(String[] args) {
        check(Grading.gradeOf("Senior engineer, mentored juniors").equals(Optional.of("senior")), "senior beats junior");
        System.out.println("GradingTest: ok");
    }

    private static void check(boolean passed, String name) {
        if (!passed) {
            throw new AssertionError(name);
        }
    }
}

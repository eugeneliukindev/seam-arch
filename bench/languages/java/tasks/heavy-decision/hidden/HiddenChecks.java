import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Optional;
import resumes.App;

public final class HiddenChecks {
    public static void main(String[] args) throws Exception {
        switch (args[0]) {
            case "summary" -> {
                Path resume = Files.createTempFile("cv", ".txt");
                Files.writeString(resume, "Senior Java developer");
                var summary = App.buildService().summarize(resume);
                Object grade = summary.grade();
                if (grade instanceof Optional<?> optional) {
                    grade = optional.orElse(null);
                }
                Object words = summary.words();
                expect("senior".equals(grade), "grade senior, got " + grade);
                expect(((Number) words).longValue() == 3, "3 words, got " + words);
            }
            default -> throw new IllegalArgumentException(args[0]);
        }
    }

    private static void expect(boolean passed, String message) {
        if (!passed) {
            throw new AssertionError(message);
        }
    }
}

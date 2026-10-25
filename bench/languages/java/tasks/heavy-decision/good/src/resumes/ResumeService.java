package resumes;

import java.nio.file.Path;
import java.util.function.Function;

/** Summarizes resumes; how a file is read is passed in. */
public final class ResumeService {
    private final Function<Path, String> read;

    public ResumeService(Function<Path, String> read) {
        this.read = read;
    }

    /** The grade the resume names and its length in words. */
    public Summary summarize(Path path) {
        String text = read.apply(path);
        String trimmed = text.strip();
        return new Summary(Grading.gradeOf(text), trimmed.isEmpty() ? 0 : trimmed.split("\\s+").length);
    }
}

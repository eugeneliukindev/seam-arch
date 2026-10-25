package resumes;

import java.nio.file.Path;

/** Summarizes resumes from disk. */
public final class ResumeService {
    /** The grade the resume names and its length in words. */
    public Summary summarize(Path path) {
        String text = ResumeFiles.readTextFile(path);
        String trimmed = text.strip();
        return new Summary(Grading.gradeOf(text), trimmed.isEmpty() ? 0 : trimmed.split("\\s+").length);
    }
}

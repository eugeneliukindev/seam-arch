package resumes;

import java.io.IOException;
import java.io.UncheckedIOException;
import java.nio.file.Files;
import java.nio.file.Path;

/** Resume files on disk. */
public final class ResumeFiles {
    private ResumeFiles() {
    }

    /** The text of a resume file. */
    public static String readTextFile(Path path) {
        try {
            return Files.readString(path);
        } catch (IOException error) {
            throw new UncheckedIOException(error);
        }
    }
}

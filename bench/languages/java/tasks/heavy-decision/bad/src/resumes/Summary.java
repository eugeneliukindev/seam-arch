package resumes;

import java.util.Optional;

/** A resume in two numbers. */
public record Summary(Optional<String> grade, int words) {
}

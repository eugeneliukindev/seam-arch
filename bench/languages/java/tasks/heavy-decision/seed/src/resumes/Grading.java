package resumes;

import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.regex.Pattern;

/** How senior a resume reads. */
public final class Grading {
    private static final List<Map.Entry<String, Pattern>> GRADES = List.of(
            Map.entry("lead", Pattern.compile("\\b(?:lead|principal|head\\s+of)\\b", Pattern.CASE_INSENSITIVE)),
            Map.entry("senior", Pattern.compile("\\b(?:senior|sr\\.?)\\b", Pattern.CASE_INSENSITIVE)),
            Map.entry("middle", Pattern.compile("\\b(?:middle|mid)\\b", Pattern.CASE_INSENSITIVE)),
            Map.entry("junior", Pattern.compile("\\b(?:junior|jr\\.?|intern)\\b", Pattern.CASE_INSENSITIVE)));

    private Grading() {
    }

    /** The highest grade the resume names; slow on long resumes, since every rule scans the whole text. */
    public static Optional<String> gradeOf(String text) {
        return GRADES.stream().filter(grade -> grade.getValue().matcher(text).find()).map(Map.Entry::getKey).findFirst();
    }
}

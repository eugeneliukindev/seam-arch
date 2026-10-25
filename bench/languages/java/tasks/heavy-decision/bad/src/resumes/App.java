package resumes;

/** Builds the resume services. */
public final class App {
    private App() {
    }

    /** A service reading resumes from disk. */
    public static ResumeService buildService() {
        return new ResumeService();
    }
}

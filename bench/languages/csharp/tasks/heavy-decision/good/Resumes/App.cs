namespace Resumes;

/// <summary>Builds the resume services.</summary>
public static class App
{
    /// <summary>A service reading resumes from disk.</summary>
    public static ResumeService BuildService() => new(ResumeFiles.ReadTextFile);
}

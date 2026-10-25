namespace Resumes;

/// <summary>Resume files on disk.</summary>
public static class ResumeFiles
{
    /// <summary>The text of a resume file.</summary>
    public static string ReadTextFile(string path) => File.ReadAllText(path);
}

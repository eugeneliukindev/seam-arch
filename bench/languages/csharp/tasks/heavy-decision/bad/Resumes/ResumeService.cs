namespace Resumes;

/// <summary>A resume in two numbers.</summary>
public sealed record Summary(string? Grade, int Words);

/// <summary>Summarizes resumes from disk.</summary>
public sealed class ResumeService
{
    /// <summary>The grade the resume names and its length in words.</summary>
    public Summary Summarize(string path)
    {
        var text = ResumeFiles.ReadTextFile(path);
        return new Summary(Grading.GradeOf(text), text.Split((char[]?)null, StringSplitOptions.RemoveEmptyEntries).Length);
    }
}

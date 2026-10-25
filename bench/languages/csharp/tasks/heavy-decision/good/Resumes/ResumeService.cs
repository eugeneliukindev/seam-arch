namespace Resumes;

/// <summary>A resume in two numbers.</summary>
public sealed record Summary(string? Grade, int Words);

/// <summary>Summarizes resumes; how a file is read is passed in.</summary>
public sealed class ResumeService(Func<string, string> read)
{
    /// <summary>The grade the resume names and its length in words.</summary>
    public Summary Summarize(string path)
    {
        var text = read(path);
        return new Summary(Grading.GradeOf(text), text.Split((char[]?)null, StringSplitOptions.RemoveEmptyEntries).Length);
    }
}

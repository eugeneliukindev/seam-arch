using System.Text.RegularExpressions;

namespace Resumes;

/// <summary>How senior a resume reads.</summary>
public static class Grading
{
    private static readonly (string Grade, Regex Pattern)[] Grades =
    [
        ("lead", new Regex(@"\b(?:lead|principal|head\s+of)\b", RegexOptions.IgnoreCase)),
        ("senior", new Regex(@"\b(?:senior|sr\.?)\b", RegexOptions.IgnoreCase)),
        ("middle", new Regex(@"\b(?:middle|mid)\b", RegexOptions.IgnoreCase)),
        ("junior", new Regex(@"\b(?:junior|jr\.?|intern)\b", RegexOptions.IgnoreCase)),
    ];

    /// <summary>
    /// The highest grade the resume names, or <c>null</c>; slow on long resumes, since every rule scans the whole text.
    /// </summary>
    public static string? GradeOf(string text) =>
        Grades.Where(rule => rule.Pattern.IsMatch(text)).Select(rule => rule.Grade).FirstOrDefault();
}

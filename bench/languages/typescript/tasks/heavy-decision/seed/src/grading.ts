/** How senior a resume reads. */

const GRADES: ReadonlyArray<readonly [string, RegExp]> = [
  ["lead", /\b(?:lead|principal|head\s+of)\b/i],
  ["senior", /\b(?:senior|sr\.?)\b/i],
  ["middle", /\b(?:middle|mid)\b/i],
  ["junior", /\b(?:junior|jr\.?|intern)\b/i],
];

/** The highest grade the resume names, or `null`; slow on long resumes, since every rule scans the whole text. */
export function gradeOf(text: string): string | null {
  return GRADES.find(([, pattern]) => pattern.test(text))?.[0] ?? null;
}

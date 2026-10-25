/** What a resume says about its author. */

import { readTextFile } from "./files.ts";
import { gradeOf } from "./grading.ts";

/** A resume in two numbers. */
export interface Summary {
  readonly grade: string | null;
  readonly words: number;
}

/** Summarizes resumes from disk. */
export class ResumeService {
  /** The grade the resume names and its length in words. */
  summarize(path: string): Summary {
    const text = readTextFile(path);
    return { grade: gradeOf(text), words: text.split(/\s+/).filter(Boolean).length };
  }
}

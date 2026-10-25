/** What a resume says about its author. */

import { gradeOf } from "./grading.ts";

/** A resume in two numbers. */
export interface Summary {
  readonly grade: string | null;
  readonly words: number;
}

/** Summarizes resumes; how a file is read is passed in. */
export class ResumeService {
  constructor(private readonly read: (path: string) => string) {}

  /** The grade the resume names and its length in words. */
  summarize(path: string): Summary {
    const text = this.read(path);
    return { grade: gradeOf(text), words: text.split(/\s+/).filter(Boolean).length };
  }
}

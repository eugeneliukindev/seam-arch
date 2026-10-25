/** Builds the resume services. */

import { readTextFile } from "./files.ts";
import { ResumeService } from "./service.ts";

/** A service reading resumes from disk. */
export function buildService(): ResumeService {
  return new ResumeService(readTextFile);
}

/** Builds the resume services. */

import { ResumeService } from "./service.ts";

/** A service reading resumes from disk. */
export function buildService(): ResumeService {
  return new ResumeService();
}

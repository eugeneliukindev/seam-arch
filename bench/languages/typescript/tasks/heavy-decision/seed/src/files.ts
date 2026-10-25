/** Resume files on disk. */

import { readFileSync } from "node:fs";

/** The text of a resume file. */
export function readTextFile(path: string): string {
  return readFileSync(path, "utf8");
}

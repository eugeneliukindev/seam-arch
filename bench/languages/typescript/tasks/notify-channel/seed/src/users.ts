/** The people alerts go to. */

/** A user who receives alerts. */
export interface User {
  readonly id: number;
  readonly email: string;
  readonly phone?: string;
}

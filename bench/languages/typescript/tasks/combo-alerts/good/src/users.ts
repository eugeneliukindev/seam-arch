/** The people alerts go to. */

/** How a user chose to get alerts. */
export type Channel = "email" | "sms" | "push";

/** A user who receives alerts, by the channel they chose; mail when they chose none. */
export interface User {
  readonly id: number;
  readonly email: string;
  readonly phone?: string;
  readonly deviceToken?: string;
  readonly channel?: Channel;
}

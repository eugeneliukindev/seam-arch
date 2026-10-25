/** Alerts delivered by mail. */

import type { SmtpClient } from "./gateways.ts";
import type { User } from "./users.ts";

/** Delivers an alert to a user's mailbox. */
export class EmailNotifier {
  constructor(private readonly smtp: SmtpClient) {}

  /** Mail `text` to `user`. */
  notify(user: User, text: string): void {
    this.smtp.sendMail(user.email, "Alert", text);
  }
}

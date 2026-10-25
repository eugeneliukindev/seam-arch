/** Raising alerts. */

import type { EmailNotifier } from "./email.ts";
import type { User } from "./users.ts";

/** Raises alerts for users. */
export class AlertService {
  constructor(private readonly notifier: EmailNotifier) {}

  /** Deliver `text` to `user`. */
  alert(user: User, text: string): void {
    this.notifier.notify(user, text);
  }
}

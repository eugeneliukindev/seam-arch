/** Raising alerts. */

import type { Channel, User } from "./users.ts";

/** Delivers an alert by one channel. */
export interface Notifier {
  /** Deliver `text` to `user`. */
  notify(user: User, text: string): void;
}

/** Raises alerts for users, each by the channel they chose. */
export class AlertService {
  constructor(private readonly notifiers: Readonly<Record<Channel, Notifier>>) {}

  /** Deliver `text` to `user`. */
  alert(user: User, text: string): void {
    this.notifiers[user.channel ?? "email"].notify(user, text);
  }
}

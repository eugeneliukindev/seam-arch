/** Raising alerts. */

import type { EmailNotifier } from "./email.ts";
import type { SmsGateway } from "./gateways.ts";
import type { User } from "./users.ts";

/** Raises alerts for users. */
export class AlertService {
  constructor(
    private readonly notifier: EmailNotifier,
    private readonly sms: SmsGateway,
  ) {}

  /** Deliver `text` to `user`. */
  alert(user: User, text: string): void {
    if (user.channel === "sms" && user.phone) {
      this.sms.send(user.phone, text);
    } else {
      this.notifier.notify(user, text);
    }
  }
}

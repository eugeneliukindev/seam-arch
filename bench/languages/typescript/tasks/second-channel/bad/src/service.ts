/** Raising alerts. */

import type { EmailNotifier } from "./email.ts";
import type { PushGateway, SmsGateway } from "./gateways.ts";
import type { User } from "./users.ts";

/** Raises alerts for users. */
export class AlertService {
  constructor(
    private readonly notifier: EmailNotifier,
    private readonly sms: SmsGateway,
    private readonly push: PushGateway,
  ) {}

  /** Deliver `text` to `user`. */
  alert(user: User, text: string): void {
    if (user.channel === "sms" && user.phone) {
      this.sms.send(user.phone, text);
    } else if (user.channel === "push" && user.deviceToken) {
      this.push.send(user.deviceToken, text);
    } else {
      this.notifier.notify(user, text);
    }
  }
}

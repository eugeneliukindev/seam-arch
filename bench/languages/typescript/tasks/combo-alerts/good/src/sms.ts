/** Alerts delivered by text message. */

import type { SmsGateway } from "./gateways.ts";
import type { Notifier } from "./service.ts";
import type { User } from "./users.ts";

/** Delivers an alert to a user's phone, or by the fallback when there is no phone. */
export class SmsNotifier implements Notifier {
  constructor(
    private readonly gateway: SmsGateway,
    private readonly fallback: Notifier,
  ) {}

  /** Text `text` to `user`. */
  notify(user: User, text: string): void {
    if (user.phone === undefined) {
      this.fallback.notify(user, text);
      return;
    }
    this.gateway.send(user.phone, text);
  }
}

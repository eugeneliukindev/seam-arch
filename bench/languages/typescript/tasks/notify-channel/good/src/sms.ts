/** Alerts delivered by text message. */

import type { SmsGateway } from "./gateways.ts";
import type { Notifier } from "./service.ts";
import type { User } from "./users.ts";

/** Delivers an alert to a user's phone. */
export class SmsNotifier implements Notifier {
  constructor(private readonly gateway: SmsGateway) {}

  /** Text `text` to `user`. */
  notify(user: User, text: string): void {
    if (user.phone === undefined) {
      throw new Error(`user ${user.id} chose text messages but has no phone`);
    }
    this.gateway.send(user.phone, text);
  }
}

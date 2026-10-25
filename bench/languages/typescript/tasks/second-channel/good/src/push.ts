/** Alerts delivered to the phone app. */

import type { PushGateway } from "./gateways.ts";
import type { Notifier } from "./service.ts";
import type { User } from "./users.ts";

/** Delivers an alert to a user's phone app. */
export class PushNotifier implements Notifier {
  constructor(private readonly gateway: PushGateway) {}

  /** Push `text` to `user`'s app. */
  notify(user: User, text: string): void {
    if (user.deviceToken === undefined) {
      throw new Error(`user ${user.id} chose push but has no device`);
    }
    this.gateway.send(user.deviceToken, text);
  }
}

/** Alerts delivered to the phone app. */

import type { PushGateway } from "./gateways.ts";
import type { Notifier } from "./service.ts";
import type { User } from "./users.ts";

/** Delivers an alert to a user's phone app, or by the fallback when there is no device. */
export class PushNotifier implements Notifier {
  constructor(
    private readonly gateway: PushGateway,
    private readonly fallback: Notifier,
  ) {}

  /** Push `text` to `user`'s app. */
  notify(user: User, text: string): void {
    if (user.deviceToken === undefined) {
      this.fallback.notify(user, text);
      return;
    }
    this.gateway.send(user.deviceToken, text);
  }
}

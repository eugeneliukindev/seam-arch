/** Builds the alert service from the delivery clients. */

import { EmailNotifier } from "./email.ts";
import type { PushGateway, SmsGateway, SmtpClient } from "./gateways.ts";
import { PushNotifier } from "./push.ts";
import { AlertService } from "./service.ts";
import { SmsNotifier } from "./sms.ts";

/** The alert service the application uses. */
export function buildService(smtp: SmtpClient, sms: SmsGateway, push: PushGateway): AlertService {
  const email = new EmailNotifier(smtp);
  return new AlertService({ email, sms: new SmsNotifier(sms, email), push: new PushNotifier(push, email) });
}

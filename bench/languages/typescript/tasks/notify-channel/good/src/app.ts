/** Builds the alert service from the delivery clients. */

import { EmailNotifier } from "./email.ts";
import type { SmsGateway, SmtpClient } from "./gateways.ts";
import { AlertService } from "./service.ts";
import { SmsNotifier } from "./sms.ts";

/** The alert service the application uses. */
export function buildService(smtp: SmtpClient, sms: SmsGateway): AlertService {
  return new AlertService({ email: new EmailNotifier(smtp), sms: new SmsNotifier(sms) });
}

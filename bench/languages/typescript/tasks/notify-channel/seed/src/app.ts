/** Builds the alert service from the delivery clients. */

import { EmailNotifier } from "./email.ts";
import type { SmsGateway, SmtpClient } from "./gateways.ts";
import { AlertService } from "./service.ts";

/** The alert service the application uses. */
export function buildService(smtp: SmtpClient, sms: SmsGateway): AlertService {
  return new AlertService(new EmailNotifier(smtp));
}

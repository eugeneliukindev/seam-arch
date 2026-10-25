/** Clients of the services that deliver messages. */

/** Sends mail through the mail relay. */
export class SmtpClient {
  /** Hand one message to the relay. */
  sendMail(to: string, subject: string, body: string): void {
    throw new Error("the relay is configured in production");
  }
}

/** Sends text messages through the SMS provider. */
export class SmsGateway {
  /** Hand one text message to the provider. */
  send(phone: string, text: string): void {
    throw new Error("the provider is configured in production");
  }
}

/** Sends notifications to the phone app through the push provider. */
export class PushGateway {
  /** Hand one notification to the provider. */
  send(deviceToken: string, text: string): void {
    throw new Error("the provider is configured in production");
  }
}

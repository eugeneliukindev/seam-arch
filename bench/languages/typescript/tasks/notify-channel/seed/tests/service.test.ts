import assert from "node:assert/strict";
import { test } from "node:test";

import { buildService } from "../src/app.ts";
import { SmsGateway, SmtpClient } from "../src/gateways.ts";

class FakeSmtp extends SmtpClient {
  readonly sent: Array<[string, string]> = [];

  override sendMail(to: string, subject: string, body: string): void {
    this.sent.push([to, body]);
  }
}

test("alert by mail", () => {
  const smtp = new FakeSmtp();
  buildService(smtp, new SmsGateway()).alert({ id: 1, email: "a@example.com" }, "disk full");
  assert.deepEqual(smtp.sent, [["a@example.com", "disk full"]]);
});

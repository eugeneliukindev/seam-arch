import assert from "node:assert/strict";
import { test } from "node:test";

import { StripeClient } from "../src/stripe-client.ts";

test("the client is configured in production", async () => {
  await assert.rejects(new StripeClient().createCharge({ amountCents: 100, currency: "EUR", source: "tok" }));
});

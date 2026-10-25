import assert from "node:assert/strict";
import { test } from "node:test";

import { describeOrder } from "../src/orders.ts";

test("order on a receipt", () => {
  assert.equal(describeOrder({ id: 1, total: 9.99, currency: "EUR" }), "Order 1: 9.99 EUR");
});

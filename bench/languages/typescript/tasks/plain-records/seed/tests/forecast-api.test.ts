import assert from "node:assert/strict";
import { test } from "node:test";

import { ForecastApi } from "../src/forecast-api.ts";

test("fetch needs the provider", async () => {
  await assert.rejects(new ForecastApi().fetch("Oslo"));
});

import assert from "node:assert/strict";
import { test } from "node:test";

import { buildService } from "../src/app.ts";

test("unknown email has no account", () => {
  assert.equal(buildService().find("nobody@example.com"), undefined);
});

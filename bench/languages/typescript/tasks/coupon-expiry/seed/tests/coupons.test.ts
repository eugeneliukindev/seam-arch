import { test } from "node:test";

import { buildBook } from "../src/app.ts";

test("add", () => {
  buildBook().add({ code: "A", percent: 10, expires: new Date("2100-01-01T00:00:00Z") });
});

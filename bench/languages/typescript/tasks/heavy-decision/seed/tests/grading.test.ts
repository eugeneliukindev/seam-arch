import assert from "node:assert/strict";
import { test } from "node:test";

import { gradeOf } from "../src/grading.ts";

test("senior beats junior", () => {
  assert.equal(gradeOf("Senior engineer, mentored juniors"), "senior");
});

/** What can be done with an account. */

import { randomBytes, scryptSync, timingSafeEqual } from "node:crypto";

import type { User, UserStore } from "./users.ts";

/** Finds and creates accounts. */
export class AccountService {
  constructor(
    private readonly users: UserStore,
    private readonly saltSize = 16,
  ) {}

  /** The account with this email, or `undefined`. */
  find(email: string): User | undefined {
    return this.users.find(email);
  }

  /** Create an account that logs in with `password`. */
  register(email: string, password: string): void {
    const salt = randomBytes(this.saltSize);
    const digest = scryptSync(password, salt, 64);
    this.users.save({ email, passwordHash: `${salt.toString("hex")}:${digest.toString("hex")}` });
  }

  /** Whether `password` is the one this account was created with. */
  logIn(email: string, password: string): boolean {
    const user = this.users.find(email);
    if (user === undefined) {
      return false;
    }
    const [salt = "", digest = ""] = user.passwordHash.split(":");
    const expected = Buffer.from(digest, "hex");
    const actual = scryptSync(password, Buffer.from(salt, "hex"), 64);
    return actual.length === expected.length && timingSafeEqual(actual, expected);
  }
}

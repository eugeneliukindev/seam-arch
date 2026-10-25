/** Password hashing: the contract and its implementation. */

import { randomBytes, scryptSync, timingSafeEqual } from "node:crypto";

/** Turns a password into a stored hash and checks one against it. */
export interface PasswordHasher {
  /** A new hash of `password`, different each call. */
  hash(password: string): string;
  /** Whether `password` produced `stored`. */
  verify(password: string, stored: string): boolean;
}

/** Salted scrypt; the stored hash is `salt:digest`, both in hex. */
export class ScryptHasher implements PasswordHasher {
  private readonly keyLength: number;
  private readonly saltSize: number;

  constructor({ keyLength = 64, saltSize = 16 }: { keyLength?: number; saltSize?: number } = {}) {
    this.keyLength = keyLength;
    this.saltSize = saltSize;
  }

  hash(password: string): string {
    const salt = randomBytes(this.saltSize);
    return `${salt.toString("hex")}:${this.digest(password, salt).toString("hex")}`;
  }

  verify(password: string, stored: string): boolean {
    const [salt = "", digest = ""] = stored.split(":");
    const expected = Buffer.from(digest, "hex");
    const actual = this.digest(password, Buffer.from(salt, "hex"));
    return actual.length === expected.length && timingSafeEqual(actual, expected);
  }

  private digest(password: string, salt: Buffer): Buffer {
    return scryptSync(password, salt, this.keyLength);
  }
}

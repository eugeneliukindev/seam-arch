/** What can be done with an account. */

import type { PasswordHasher } from "./hashing.ts";
import type { User, UserStore } from "./users.ts";

/** Finds and creates accounts. */
export class AccountService {
  constructor(
    private readonly users: UserStore,
    private readonly hasher: PasswordHasher,
  ) {}

  /** The account with this email, or `undefined`. */
  find(email: string): User | undefined {
    return this.users.find(email);
  }

  /** Create an account that logs in with `password`. */
  register(email: string, password: string): void {
    this.users.save({ email, passwordHash: this.hasher.hash(password) });
  }

  /** Whether `password` is the one this account was created with. */
  logIn(email: string, password: string): boolean {
    const user = this.users.find(email);
    return user !== undefined && this.hasher.verify(password, user.passwordHash);
  }
}

/** What can be done with an account. */

import type { User, UserStore } from "./users.ts";

/** Finds and creates accounts. */
export class AccountService {
  constructor(private readonly users: UserStore) {}

  /** The account with this email, or `undefined`. */
  find(email: string): User | undefined {
    return this.users.find(email);
  }
}

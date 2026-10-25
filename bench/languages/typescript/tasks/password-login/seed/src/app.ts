/** Builds the account service. */

import { AccountService } from "./service.ts";
import { InMemoryUsers } from "./users.ts";

/** A ready service with its own store. */
export function buildService(): AccountService {
  return new AccountService(new InMemoryUsers());
}

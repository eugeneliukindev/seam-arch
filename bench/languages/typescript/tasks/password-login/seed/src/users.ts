/** Users and where they are kept. */

/** Someone with an account. */
export interface User {
  readonly email: string;
  readonly passwordHash: string;
}

/** Where users are kept. */
export interface UserStore {
  /** The user with this email, or `undefined`. */
  find(email: string): User | undefined;
  /** Store `user`, replacing one with the same email. */
  save(user: User): void;
}

/** Users kept in a map, for one process. */
export class InMemoryUsers implements UserStore {
  private readonly users = new Map<string, User>();

  find(email: string): User | undefined {
    return this.users.get(email);
  }

  save(user: User): void {
    this.users.set(user.email, user);
  }
}

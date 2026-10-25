/** Orders customers place. */

/** An order waiting for payment; `total` is in the currency's units, like 9.99. */
export interface Order {
  readonly id: number;
  readonly total: number;
  readonly currency: string;
}

/** How an order reads on a receipt. */
export function describeOrder(order: Order): string {
  return `Order ${order.id}: ${order.total.toFixed(2)} ${order.currency}`;
}

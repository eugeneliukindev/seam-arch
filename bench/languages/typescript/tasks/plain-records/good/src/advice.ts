/** What to wear and carry, from the forecast. */

import type { ForecastApi } from "./forecast-api.ts";

const RAIN_THRESHOLD = 0.5;

/** Whether rain is more likely than not in `city` today. */
export async function shouldTakeUmbrella(city: string, api: ForecastApi): Promise<boolean> {
  return (await api.today(city)).rainChance > RAIN_THRESHOLD;
}

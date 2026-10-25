/** Client of the forecast provider. */

/** Talks to the forecast provider over the network. */
export class ForecastApi {
  constructor(private readonly baseUrl = "https://forecast.example.com") {}

  /**
   * The provider's raw JSON for `city`, today first.
   *
   * For example `{"daily": [{"pop": 0.7, "tmax": 12.3}, {"pop": 0.1, "tmax": 15.0}]}`,
   * where `pop` is the probability of precipitation from 0 to 1 and `tmax` the
   * day's highest temperature in degrees Celsius.
   */
  async fetch(city: string): Promise<any> {
    throw new Error("the provider is configured in production");
  }
}

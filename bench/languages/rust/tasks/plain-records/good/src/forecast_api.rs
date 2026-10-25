//! Client of the forecast provider; configured in production.

use crate::forecast::Forecast;
use crate::json::Json;

/// Talks to the forecast provider over the network.
pub trait ForecastApi {
    /// The provider's raw JSON for `city`, today first.
    ///
    /// For example `{"daily": [{"pop": 0.7, "tmax": 12.3}, {"pop": 0.1, "tmax": 15.0}]}`,
    /// where `pop` is the probability of precipitation from 0 to 1 and `tmax` the
    /// day's highest temperature in degrees Celsius.
    fn fetch(&self, city: &str) -> Json;

    /// Today's forecast for `city`; no chance of rain when the provider gives none.
    fn today(&self, city: &str) -> Forecast {
        Forecast { rain_chance: self.fetch(city)["daily"][0]["pop"].as_f64().unwrap_or(0.0) }
    }
}

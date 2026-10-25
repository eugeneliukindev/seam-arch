//! What to wear and carry, from the forecast.

use crate::forecast_api::ForecastApi;

/// Above this chance of rain, take an umbrella.
const RAIN_THRESHOLD: f64 = 0.5;

/// Whether rain is more likely than not in `city` today.
pub fn should_take_umbrella(city: &str, api: &dyn ForecastApi) -> bool {
    api.today(city).rain_chance > RAIN_THRESHOLD
}

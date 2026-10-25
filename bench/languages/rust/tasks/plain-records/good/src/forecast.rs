//! The forecast as the app sees it.

/// Today's weather in one city.
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct Forecast {
    /// The chance of rain, from 0 to 1.
    pub rain_chance: f64,
}

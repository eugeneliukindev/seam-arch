use std::collections::BTreeMap;

use weather::advice::should_take_umbrella;
use weather::forecast_api::ForecastApi;
use weather::json::Json;

/// The provider answering with a fixed payload.
struct FakeApi {
    payload: Json,
}

impl FakeApi {
    fn new(rain_chance: f64) -> Self {
        let day = |pop: f64, tmax: f64| {
            Json::Object(BTreeMap::from([("pop".to_owned(), Json::Number(pop)), ("tmax".to_owned(), Json::Number(tmax))]))
        };
        let daily = Json::Array(vec![day(rain_chance, 12.3), day(0.0, 15.0)]);
        Self { payload: Json::Object(BTreeMap::from([("daily".to_owned(), daily)])) }
    }
}

impl ForecastApi for FakeApi {
    fn fetch(&self, _city: &str) -> Json {
        self.payload.clone()
    }
}

#[test]
fn umbrella_advice() {
    for (rain_chance, expected) in [(0.7, true), (0.2, false)] {
        assert_eq!(should_take_umbrella("Oslo", &FakeApi::new(rain_chance)), expected, "rain chance {rain_chance}");
    }
}

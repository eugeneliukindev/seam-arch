use std::collections::BTreeMap;

use weather::json::Json;

#[test]
fn reads_members_and_items() {
    let day = Json::Object(BTreeMap::from([("pop".to_owned(), Json::Number(0.7))]));
    let payload = Json::Object(BTreeMap::from([("daily".to_owned(), Json::Array(vec![day]))]));
    assert_eq!(payload["daily"][0]["pop"].as_f64(), Some(0.7));
    assert_eq!(payload["hourly"][3], Json::Null);
}

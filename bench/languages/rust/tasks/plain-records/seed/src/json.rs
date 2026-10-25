//! JSON values as the provider's client decodes them.

use std::collections::BTreeMap;
use std::ops::Index;

/// One decoded JSON value.
#[derive(Debug, Clone, PartialEq)]
pub enum Json {
    Null,
    Bool(bool),
    Number(f64),
    String(String),
    Array(Vec<Json>),
    Object(BTreeMap<String, Json>),
}

const NULL: Json = Json::Null;

impl Json {
    /// The member `key` of an object.
    pub fn get(&self, key: &str) -> Option<&Json> {
        match self {
            Self::Object(members) => members.get(key),
            _ => None,
        }
    }

    /// The items of an array.
    pub fn as_array(&self) -> Option<&[Json]> {
        match self {
            Self::Array(items) => Some(items),
            _ => None,
        }
    }

    /// The value of a number.
    pub fn as_f64(&self) -> Option<f64> {
        match self {
            Self::Number(number) => Some(*number),
            _ => None,
        }
    }
}

/// The member `key` of an object; `Json::Null` when there is none.
impl Index<&str> for Json {
    type Output = Json;

    fn index(&self, key: &str) -> &Json {
        self.get(key).unwrap_or(&NULL)
    }
}

/// The item at `position` of an array; `Json::Null` when there is none.
impl Index<usize> for Json {
    type Output = Json;

    fn index(&self, position: usize) -> &Json {
        self.as_array().and_then(|items| items.get(position)).unwrap_or(&NULL)
    }
}

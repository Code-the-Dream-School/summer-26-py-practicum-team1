import pytest

from pipeline.transform.openweather import transform_air_pollution


def test_transform_returns_clean_record():
  raw_response = {
    "coord": {
      "lat": 50,
      "lon": 50,
    },
    "list": [
      {
        "dt": 1606489200,
        "main": {
          "aqi": 1,
        },
        "components": {
          "pm2_5": 0.9,
          "pm10": 0.93,
          "no2": 2.29,
          "o3": 46.49,
        },
      }
    ],
  }

  location = {
    "city": "Raleigh",
    "country_code": "US",
    "state": "NC",
  }

  result = transform_air_pollution(raw_response, location)

  assert result == [
    {
      "location": "Raleigh, US, NC",
      "latitude": 50,
      "longitude": 50,
      "observed_at": 1606489200,
      "aqi": 1,
      "pm2_5": 0.9,
      "pm10": 0.93,
      "no2": 2.29,
      "o3": 46.49,
    }
  ]


def test_transform_empty_observations_returns_empty_list():
  raw_response = {
    "coord": {
      "lat": 50,
      "lon": 50,
    },
    "list": [],
  }

  location = {
    "city": "Paris",
    "country_code": "FR",
    "state": "",
  }

  assert transform_air_pollution(raw_response, location) == []


def test_transform_rejects_string_coordinates():
  raw_response = {
    "coord": {
      "lat": "50",
      "lon": "50",
    },
    "list": [
      {
        "dt": 1606489200,
        "main": {"aqi": 1},
        "components": {},
      }
    ],
  }

  location = {
    "city": "Paris",
    "country_code": "FR",
    "state": "",
  }

  with pytest.raises(
    ValueError,
    match="Latitude and longitude must be numeric",
  ):
    transform_air_pollution(raw_response, location)


def test_transform_rejects_out_of_range_longitude():
  raw_response = {
    "coord": {
      "lat": 50,
      "lon": 4000,
    },
    "list": [
        {
          "dt": 1606489200,
          "main": {"aqi": 1},
          "components": {},
        }
    ],
  }

  location = {
    "city": "Paris",
    "country_code": "FR",
    "state": "",
  }

  with pytest.raises(
    ValueError,
    match="Longitude is out of range",
  ):
      transform_air_pollution(raw_response, location)
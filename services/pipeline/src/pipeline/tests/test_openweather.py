import pytest

from unittest.mock import patch

from pipeline.extract.openweather import geocode_location

from pipeline.extract.openweather import (
  geocode_location,
  fetch_air_pollution_history,
)

def test_fetch_air_pollution_history_empty_response(monkeypatch):
  monkeypatch.setenv(
    "OPENWEATHER_API_KEY",
    "test-key",
  )

  with patch(
    "pipeline.extract.openweather._get_json",
    return_value={"list": []},
  ):
    with pytest.raises(
      ValueError,
      match="No air pollution data returned",
    ):
      fetch_air_pollution_history(
        lat=35.2271,
        lon=-80.8431,
        start=1606480000,
        end=1606485000,
      )

def test_geocode_location_returns_coordinates(monkeypatch):
  location = {
    "city": "Charlotte",
    "country_code": "US",
    "state": "NC",
  }

  fake_response = [
    {
      "lat": 35.2271,
      "lon": -80.8431,
      "name": "Charlotte",
      "country": "US",
      "state": "North Carolina",
    }
  ]

  monkeypatch.setenv(
    "OPENWEATHER_API_KEY",
    "test-key",
  )

  with patch(
    "pipeline.extract.openweather._get_json",
    return_value=fake_response,
  ):
    result = geocode_location(location)

  assert result == {
    "lat": 35.2271,
    "lon": -80.8431,
  }

def test_geocode_location_not_found(monkeypatch):
  location = {
    "city": "UnknownCity",
    "country_code": "US",
    "state": "",
  }

  monkeypatch.setenv(
    "OPENWEATHER_API_KEY",
    "test-key",
  )

  with patch(
    "pipeline.extract.openweather._get_json",
    return_value=[],
  ):
    try:
      geocode_location(location)
      assert False
    except ValueError as exc:
      assert "Location not found" in str(exc)




def test_fetch_air_pollution_history_returns_data(monkeypatch):
  monkeypatch.setenv(
    "OPENWEATHER_API_KEY",
    "test-key",
  )

  fake_response = {
    "coord": {
        "lon": -80.8431,
        "lat": 35.2271,
    },
    "list": [
      {
        "dt": 1606482000,
        "main": {
          "aqi": 2,
        },
        "components": {
          "pm2_5": 13.448,
          "pm10": 15.524,
          "no2": 43.184,
          "o3": 4.783,
        },
      }
    ],
  }

  with patch(
    "pipeline.extract.openweather._get_json",
    return_value=fake_response,
  ):
    result = fetch_air_pollution_history(
      lat=35.2271,
      lon=-80.8431,
      start=1606480000,
      end=1606485000,
    )

  assert result == fake_response
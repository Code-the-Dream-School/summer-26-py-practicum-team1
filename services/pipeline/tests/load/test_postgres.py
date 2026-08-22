from datetime import datetime, timezone

from pipeline.load.postgres import prepare_air_quality_values


def test_prepare_air_quality_values_selects_database_record_fields():
    observed_at = datetime(2020, 11, 27, 13, 0, tzinfo=timezone.utc)
    transformed_record = {
        "location": "Charlotte, US, NC",
        "latitude": 35.2271,
        "longitude": -80.8431,
        "observed_at": observed_at,
        "aqi": 2,
        "pm2_5": 13.448,
        "pm10": 15.524,
        "no2": 43.184,
        "o3": 4.783,
    }

    values = prepare_air_quality_values(transformed_record)

    assert values == {
        "observed_at": observed_at,
        "aqi": 2,
        "pm2_5": 13.448,
        "pm10": 15.524,
        "no2": 43.184,
        "o3": 4.783,
    }


def test_prepare_air_quality_values_maps_missing_optional_pollutants_to_none():
    observed_at = datetime(2020, 11, 27, 13, 0, tzinfo=timezone.utc)
    transformed_record = {
        "location": "Charlotte, US, NC",
        "latitude": 35.2271,
        "longitude": -80.8431,
        "observed_at": observed_at,
        "aqi": 2,
    }

    values = prepare_air_quality_values(transformed_record)

    assert values == {
        "observed_at": observed_at,
        "aqi": 2,
        "pm2_5": None,
        "pm10": None,
        "no2": None,
        "o3": None,
    }

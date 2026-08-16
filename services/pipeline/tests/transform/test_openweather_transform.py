"""SCRUM-29 - Automated Transform Tests.

Tests for:
    services/pipeline/src/pipeline/transform/openweather.py

Based on the Sprint 3 transform contract, data dictionary, normalization
rules, and SCRUM-29 acceptance criteria.

The tests use sanitized OpenWeather samples only. They do not call the live
API and do not write to a database.
"""

from datetime import datetime, timezone
import pytest
from pipeline.transform.openweather import transform_air_pollution

@pytest.fixture
def location_context():
    return {
        "city": "Raleigh",
        "country_code": "US",
        "state": "NC",
    }

@pytest.fixture
def representative_raw_response():
    """Sanitized Sprint 2 OpenWeather Historical Air Pollution sample."""
    return {
        "coord": {
            "lon": 50,
            "lat": 50,
        },
        "list": [
            {
                "main": {
                    "aqi": 1,
                },
                "components": {
                    "co": 226.97,
                    "no": 0,
                    "no2": 2.29,
                    "o3": 46.49,
                    "so2": 0.95,
                    "pm2_5": 0.90,
                    "pm10": 0.93,
                    "nh3": 0.09,
                },
                "dt": 1606489200,
            }
        ],
    }

# main test
def test_transform_representative_successful_response(
    representative_raw_response,
    location_context,
):
    """A representative response must match the agreed clean contract."""
    records = transform_air_pollution(
        representative_raw_response,
        location_context,
    )

    assert isinstance(records, list)
    assert len(records) == 1

    record = records[0]

    assert set(record) == {
        "location",
        "latitude",
        "longitude",
        "observed_at",
        "aqi",
        "pm2_5",
        "pm10",
        "no2",
        "o3",
    }

    assert record["location"] == "Raleigh, US, NC"

    # Numeric types are normalized for the clean dataset.
    assert record["latitude"] == 50.0
    assert record["longitude"] == 50.0
    assert isinstance(record["latitude"], float)
    assert isinstance(record["longitude"], float)

    # Unix seconds are normalized to a timezone-aware UTC datetime.
    assert record["observed_at"] == datetime(
        2020,
        11,
        27,
        15,
        0,
        tzinfo=timezone.utc,
    )
    assert record["observed_at"].tzinfo == timezone.utc

    assert record["aqi"] == 1
    assert isinstance(record["aqi"], int)

    assert record["pm2_5"] == pytest.approx(0.90)
    assert record["pm10"] == pytest.approx(0.93)
    assert record["no2"] == pytest.approx(2.29)
    assert record["o3"] == pytest.approx(46.49)

    assert isinstance(record["pm2_5"], float)
    assert isinstance(record["pm10"], float)
    assert isinstance(record["no2"], float)
    assert isinstance(record["o3"], float)


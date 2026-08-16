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


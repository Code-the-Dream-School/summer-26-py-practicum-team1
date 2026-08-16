import logging
from datetime import datetime, timezone

import pytest

from pipeline.transform.openweather import transform_air_pollution


COMPONENTS = {
    "co": 270.367,
    "no": 5.867,
    "no2": 43.184,
    "o3": 4.783,
    "so2": 14.544,
    "pm2_5": 13.448,
    "pm10": 15.524,
    "nh3": 0.289,
}

EXPECTED_FIELDS = {
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


def make_observation(dt=1606482000, aqi=2, components=None):
    return {
        "dt": dt,
        "main": {"aqi": aqi},
        "components": COMPONENTS.copy() if components is None else components,
    }


def make_payload(observations):
    return {
        "coord": {"lat": 35.2271, "lon": -80.8431},
        "list": observations,
    }


def test_valid_payload_returns_expected_clean_record():
    records = transform_air_pollution(
        make_payload([make_observation()]),
        {"city": "Charlotte", "country_code": "US", "state": "NC"},
    )

    assert records == [{
        "location": "Charlotte, US, NC",
        "latitude": 35.2271,
        "longitude": -80.8431,
        "observed_at": datetime(2020, 11, 27, 13, 0, tzinfo=timezone.utc),
        "aqi": 2,
        "pm2_5": 13.448,
        "pm10": 15.524,
        "no2": 43.184,
        "o3": 4.783,
    }]
    assert set(records[0]) == EXPECTED_FIELDS


def test_numeric_strings_are_normalized():
    components = {field: str(value) for field, value in COMPONENTS.items()}

    records = transform_air_pollution(
        {
            "coord": {"lat": "35.2271", "lon": "-80.8431"},
            "list": [make_observation(dt="1606482000", aqi="2", components=components)],
        },
        {"city": "Paris", "country_code": "FR"},
    )

    assert records[0]["location"] == "Paris, FR"
    assert records[0]["latitude"] == 35.2271
    assert records[0]["longitude"] == -80.8431
    assert records[0]["observed_at"] == datetime(2020, 11, 27, 13, 0, tzinfo=timezone.utc)
    assert records[0]["aqi"] == 2
    assert records[0]["pm2_5"] == 13.448
    assert records[0]["pm10"] == 15.524
    assert records[0]["no2"] == 43.184
    assert records[0]["o3"] == 4.783


def test_invalid_optional_pollutants_become_none_and_record_is_kept(caplog):
    components = COMPONENTS.copy()
    components.pop("pm2_5")
    components["no2"] = "not-a-number"
    components["co"] = "ignored-value"

    with caplog.at_level(logging.WARNING, logger="pipeline.transform.openweather"):
        records = transform_air_pollution(
            make_payload([make_observation(components=components)]),
            {"city": "Charlotte", "country_code": "US"},
        )

    assert len(records) == 1
    assert records[0]["pm2_5"] is None
    assert records[0]["no2"] is None
    assert "field=list[0].components.pm2_5 value=None" in caplog.text
    assert "field=list[0].components.no2 value='not-a-number'" in caplog.text
    assert "components.co" not in caplog.text


@pytest.mark.parametrize(
    "observation",
    [
        make_observation(dt=None),
        make_observation(aqi=6),
    ],
)
def test_invalid_required_dt_or_aqi_skips_observation(observation, caplog):
    with caplog.at_level(logging.WARNING, logger="pipeline.transform.openweather"):
        records = transform_air_pollution(
            make_payload([observation]),
            {"city": "Charlotte", "country_code": "US"},
        )

    assert records == []
    assert "Invalid or missing normalization value" in caplog.text


def test_invalid_observation_does_not_block_next_valid_observation():
    records = transform_air_pollution(
        make_payload([
            make_observation(aqi=6),
            make_observation(dt=1606485600, aqi=3),
        ]),
        {"city": "Charlotte", "country_code": "US"},
    )

    assert len(records) == 1
    assert records[0]["observed_at"] == datetime(2020, 11, 27, 14, 0, tzinfo=timezone.utc)
    assert records[0]["aqi"] == 3

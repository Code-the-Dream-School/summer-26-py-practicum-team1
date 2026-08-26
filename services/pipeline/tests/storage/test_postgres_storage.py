"""SCRUM-36 Storage tests and verification

- Checking empty database
"""

from datetime import datetime, timezone

import pytest
from sqlalchemy import func, inspect, select

from pipeline.load.postgres import (
    save_raw_response,
    save_transformed_records,
)
from services.database.models import (
    AirQualityRecord,
    RawApiResponse,
)


OBSERVED_AT = datetime(2020, 11, 27, 13, 0, tzinfo=timezone.utc, )

# Test for empty database
def test_migration_builds_schema_from_empty_database(test_engine):
    inspector = inspect(test_engine)

    tables = set(inspector.get_table_names())

    assert {
        "locations",
        "air_quality_records",
        "raw_api_responses",
        "pipeline_runs",
    }.issubset(tables)

# test new raw response
def test_writes_new_raw_response_and_transformed_record(db_connection, location_id, ):
    fetched_at = datetime(2020, 11, 27, 15, 0, tzinfo=timezone.utc, )

    payload = {
        "coord": {
            "lat": 35.2271,
            "lon": -80.8431,
        },
        "list": [
            {
                "dt": 1606489200,
                "main": {"aqi": 2},
                "components": {
                    "pm2_5": 13.5,
                    "pm10": 15.5,
                },
            }
        ],
    }

    transformed_record = {
        "observed_at": OBSERVED_AT,
        "aqi": 2,
        "pm2_5": 13.5,
        "pm10": 15.5,
        "no2": 43.0,
        "o3": 5.0,
    }

    save_raw_response(db_connection, location_id=location_id, fetched_at=fetched_at, payload=payload, )

    save_transformed_records(db_connection, location_id=location_id, records=[transformed_record], )

    raw_row = db_connection.execute(
        select(RawApiResponse.__table__).where(
            RawApiResponse.location_id == location_id
        )
    ).mappings().one()

    transformed_row = db_connection.execute(
        select(AirQualityRecord.__table__).where(
            AirQualityRecord.location_id == location_id,
            AirQualityRecord.observed_at == OBSERVED_AT,
        )
    ).mappings().one()

    assert raw_row["payload"] == payload
    assert raw_row["fetched_at"] == fetched_at

    assert transformed_row["aqi"] == 2
    assert transformed_row["pm2_5"] == pytest.approx(13.5)
    assert transformed_row["pm10"] == pytest.approx(15.5)


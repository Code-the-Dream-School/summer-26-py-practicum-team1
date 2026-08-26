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
"""SCRUM-36 Storage tests and verification

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
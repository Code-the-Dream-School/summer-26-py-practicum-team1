from datetime import datetime

from sqlalchemy import insert, text
from sqlalchemy.engine import Connection

from services.database.models import RawApiResponse


INSERT_AIR_QUALITY_RECORDS = text("""
    INSERT INTO air_quality_records (
        location_id,
        observed_at,
        aqi,
        pm2_5,
        pm10,
        no2,
        o3
    ) VALUES (
        :location_id,
        :observed_at,
        :aqi,
        :pm2_5,
        :pm10,
        :no2,
        :o3
    )
""")

INSERT_RAW_API_RESPONSE = insert(RawApiResponse)


def prepare_air_quality_values(record):
    """Select transformed values stored in an air quality record row."""
    return {
        "observed_at": record["observed_at"],
        "aqi": record["aqi"],
        "pm2_5": record.get("pm2_5"),
        "pm10": record.get("pm10"),
        "no2": record.get("no2"),
        "o3": record.get("o3"),
    }


def save_transformed_records(
    connection: Connection,
    location_id: int,
    records: list[dict],
) -> None:
    """Insert transformed observations for an already-resolved location."""
    values = [
        {
            "location_id": location_id,
            **prepare_air_quality_values(record),
        }
        for record in records
    ]

    if not values:
        return

    connection.execute(INSERT_AIR_QUALITY_RECORDS, values)


def save_raw_response(
    connection: Connection,
    location_id: int,
    fetched_at: datetime,
    payload: dict,
) -> None:
    """Insert a complete raw API response for an already-resolved location."""
    connection.execute(INSERT_RAW_API_RESPONSE, {
        "location_id": location_id,
        "fetched_at": fetched_at,
        "payload": payload,
    })

from datetime import datetime, timezone

import pandas as pd

from pipeline.export.parquet import (
    build_parquet_path,
    export_transformed_records,
)

def test_export_transformed_records_creates_parquet(tmp_path):
    records = [
        {
            "location": "Charlotte, US, NC",
            "latitude": 35.2271,
            "longitude": -80.8431,
            "observed_at": datetime(
                2026,
                8,
                1,
                12,
                0,
                tzinfo=timezone.utc,
            ),
            "aqi": 2,
            "pm2_5": 4.5,
            "pm10": 7.2,
            "no2": 3.1,
            "o3": 40.0,
        }
    ]

    output_path = tmp_path / "air_quality.parquet"

    result = export_transformed_records(
        records,
        output_path,
    )

    assert result == output_path
    assert output_path.exists()

    dataframe = pd.read_parquet(output_path)

    assert len(dataframe) == 1
    assert dataframe.iloc[0]["location"] == "Charlotte, US, NC"
    assert dataframe.iloc[0]["aqi"] == 2

def test_export_transformed_records_empty_records(tmp_path):
    output_path = tmp_path / "empty.parquet"

    result = export_transformed_records(
        [],
        output_path,
    )

    assert result is None
    assert not output_path.exists()


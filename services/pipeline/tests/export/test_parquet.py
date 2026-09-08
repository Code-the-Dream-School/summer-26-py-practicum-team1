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


def test_export_creates_parent_directory(tmp_path):
    output_path = (
        tmp_path
        / "nested"
        / "exports"
        / "air_quality.parquet"
    )

    records = [
        {
            "location": "Paris, FR",
            "latitude": 48.8566,
            "longitude": 2.3522,
            "observed_at": datetime(
                2026,
                8,
                1,
                12,
                0,
                tzinfo=timezone.utc,
            ),
            "aqi": 1,
            "pm2_5": 2.1,
            "pm10": 3.4,
            "no2": 5.0,
            "o3": 32.0,
        }
    ]

    export_transformed_records(
        records,
        output_path,
    )

    assert output_path.exists()


def test_build_parquet_path(monkeypatch, tmp_path):
    monkeypatch.setenv(
        "PARQUET_EXPORT_DIR",
        str(tmp_path),
    )

    result = build_parquet_path(
        "New York",
        42,
    )

    assert result == tmp_path / "new_york_run_42.parquet"


def test_build_parquet_path_sanitizes_city_name(
    monkeypatch,
    tmp_path,
):
    monkeypatch.setenv(
        "PARQUET_EXPORT_DIR",
        str(tmp_path),
    )

    result = build_parquet_path(
        "São Paulo",
        42,
    )

    assert result == tmp_path / "sao_paulo_run_42.parquet"
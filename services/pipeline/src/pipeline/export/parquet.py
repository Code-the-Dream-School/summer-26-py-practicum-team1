"""SCRUM-31

"""

import logging
from pathlib import Path
import os

import pandas as pd


logger = logging.getLogger(__name__)


DEFAULT_PARQUET_EXPORT_DIR = Path("data/exports")


def get_parquet_export_dir() -> Path:
    raw = os.getenv("PARQUET_EXPORT_DIR")
    return Path(raw) if raw else DEFAULT_PARQUET_EXPORT_DIR

def export_transformed_records(
    records: list[dict],
    output_path: Path | str,
) -> Path | None:
    """Export transformed air-quality records to a Parquet file."""

    if not records:
        logger.info("Parquet export skipped: no transformed records")
        return None

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    dataframe = pd.DataFrame(records)
    dataframe.to_parquet(
        path,
        index=False,
        engine="pyarrow",
    )

    logger.info(
        "Parquet export completed: path=%s records=%d",
        path,
        len(records),
    )

    return path


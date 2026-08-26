"""SCRUM-36 Storage tests and verification

"""

import os
import re
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, insert
from sqlalchemy.engine import make_url

from services.database.models import Location

# Alembic
REPO_ROOT = Path(__file__).resolve().parents[4]

DEFAULT_TEST_DATABASE_URL = (
    "postgresql+psycopg://postgres:postgres@localhost:5433/"
    "air_tracker_test"
)

# exists database air_tracker_test
def _ensure_test_database(database_url: str) -> None:
    url = make_url(database_url)
    database_name = url.database

    if not database_name or not database_name.endswith("_test"):
        raise RuntimeError(
            "Storage tests require a database name ending with '_test'"
        )

    if not re.fullmatch(r"[A-Za-z0-9_]+", database_name):
        raise RuntimeError("Unsafe test database name")

    admin_url = url.set(database="postgres")
    admin_engine = create_engine(
        admin_url,
        isolation_level="AUTOCOMMIT",
    )

    try:
        with admin_engine.connect() as connection:
            exists = connection.exec_driver_sql(
                "SELECT 1 FROM pg_database WHERE datname = %s",
                (database_name,),
            ).scalar()

            if not exists:
                connection.exec_driver_sql(
                    f'CREATE DATABASE "{database_name}"'
                )
    finally:
        admin_engine.dispose()

# empty database
def _reset_test_schema(database_url: str) -> None:
    engine = create_engine(
        database_url,
        isolation_level="AUTOCOMMIT",
    )

    try:
        with engine.connect() as connection:
            connection.exec_driver_sql(
                "DROP SCHEMA IF EXISTS public CASCADE"
            )
            connection.exec_driver_sql("CREATE SCHEMA public")
    finally:
        engine.dispose()

# Alembic migrations
def _apply_migrations(database_url: str) -> None:
    previous_database_url = os.environ.get("DATABASE_URL")
    os.environ["DATABASE_URL"] = database_url

    try:
        config = Config(str(REPO_ROOT / "alembic.ini"))
        command.upgrade(config, "head")
    finally:
        if previous_database_url is None:
            os.environ.pop("DATABASE_URL", None)
        else:
            os.environ["DATABASE_URL"] = previous_database_url


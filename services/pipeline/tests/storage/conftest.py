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


REPO_ROOT = Path(__file__).resolve().parents[4]

DEFAULT_TEST_DATABASE_URL = (
    "postgresql+psycopg://postgres:postgres@localhost:5433/"
    "air_tracker_test"
)
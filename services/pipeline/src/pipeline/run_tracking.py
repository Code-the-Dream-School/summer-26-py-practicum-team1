"""SCRUM-35 Pipeline run tracking

"""

from datetime import datetime, timezone

from sqlalchemy import text
from sqlalchemy.engine import Connection

FINAL_STATUSES = {"success", "failed"}

# SQL requests
INSERT_PIPELINE_RUN = text("""
    INSERT INTO pipeline_runs (
        started_at,
        status
    )
    VALUES (
        :started_at,
        'running'
    )
    RETURNING id
""")


UPDATE_PIPELINE_RUN = text("""
    UPDATE pipeline_runs
    SET
        finished_at = :finished_at,
        status = :status,
        records_processed = :records_processed,
        error_message = :error_message
    WHERE id = :run_id
""")


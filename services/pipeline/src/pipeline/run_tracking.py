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

# start pipeline run 
def start_pipeline_run(
    connection: Connection,
    started_at: datetime | None = None,
) -> int:
    """Create a new pipeline run and return its database id."""

    if started_at is None:
        started_at = datetime.now(timezone.utc)

    result = connection.execute(
        INSERT_PIPELINE_RUN,
        {
            "started_at": started_at,
        },
    )

    return result.scalar_one()


# Scheduler Workflow

The City Air Tracker scheduler uses Prefect to run the existing shared pipeline on a configured cron schedule.

Each scheduled run calculates a recent rolling historical window and passes the resulting Unix `start` and `end` timestamps to the shared `run_pipeline(...)` function. The scheduler does not implement extract, transform, or load logic itself.

## Configuration

The scheduler loads configuration from environment variables and a local `.env` file.

| Variable | Required | Purpose |
| --- | --- | --- |
| `DATABASE_URL` | Yes | SQLAlchemy connection URL for PostgreSQL |
| `PIPELINE_SCHEDULE_CRON` | Yes | Cron expression for the Prefect schedule, interpreted in UTC |
| `PIPELINE_HISTORY_HOURS` | Yes | Positive integer defining the rolling historical window for each run |
| `OPENWEATHER_API_KEY` | Yes | API key used by the OpenWeather extraction code |
| `CITIES_CSV_FILE` | No | Path to the city input CSV; defaults to `services/pipeline/config/cities.csv` |

Example local `.env`:

```dotenv
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5433/air_tracker
OPENWEATHER_API_KEY=replace-with-your-api-key
CITIES_CSV_FILE=services/pipeline/config/cities.csv
PIPELINE_SCHEDULE_CRON='0 * * * *'
PIPELINE_HISTORY_HOURS=24
```

`PIPELINE_SCHEDULE_CRON` uses standard cron syntax. The example above runs hourly, but it does not define the production schedule.

`PIPELINE_HISTORY_HOURS` controls how much recent historical data is requested on each run. For example, a value of `24` creates a rolling 24-hour window.

Before running the scheduler, complete the [Local PostgreSQL and Alembic Migration Workflow](local_postgresql_first_workflow.md).

## Run the Scheduler Locally

Start a local Prefect server in one terminal:

```bash
.venv/bin/prefect server start
```

In another terminal, start the scheduler from the repository root with the Prefect API URL configured for that command:

```bash
PREFECT_API_URL=http://127.0.0.1:4200/api \
PYTHONPATH=services/pipeline/src \
.venv/bin/python -m pipeline.scheduler
```

The scheduler serves the `city-air-tracker-scheduled-pipeline` deployment and keeps the process available for runs scheduled by `PIPELINE_SCHEDULE_CRON`.

The local Prefect UI is available at `http://127.0.0.1:4200`.

## Expected Behavior

Immediately before each scheduled run, the scheduler calculates:

- `end` as the current UTC time in Unix seconds;
- `start` as `end` minus the configured `PIPELINE_HISTORY_HOURS`.

The scheduler then:

1. reads and validates the configured city records;
2. continues with valid locations if some city records are invalid;
3. fails if no valid locations remain;
4. creates a database transaction;
5. calls the shared `run_pipeline(connection, locations, start, end)` runner;
6. disposes of the database engine after execution.

If the shared runner returns a successful result, the scheduled flow completes successfully.

If the runner returns a failed status, the database transaction completes before the scheduler raises an exception. This allows the failed pipeline status to be persisted while also causing Prefect to mark the flow run as Failed.

Other scheduler or pipeline exceptions are propagated rather than silently ignored.

## Verify a Failure

Failed flow runs are visible in the local Prefect UI at `http://127.0.0.1:4200`. The exception is available in the flow run details.

Pipeline run status can also be checked in PostgreSQL:

```sql
SELECT
    id,
    started_at,
    finished_at,
    status,
    records_processed,
    error_message
FROM pipeline_runs
ORDER BY id DESC
LIMIT 5;
```

When the shared runner returns a failed result, the corresponding pipeline run is stored with `status = 'failed'` and the available failure details in `error_message`.
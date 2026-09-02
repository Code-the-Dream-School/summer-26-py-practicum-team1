# Runtime Configuration and Secrets
The pipeline needs a few environment variables to run.

## Environment variables
The pipeline uses:
- DATABASE_URL - the connection URL for the PostgreSQL database
- OPENWEATHER_API_KEY - the API key used to access the OpenWeather API.

For local development, these values are stored in a .env file.

Example:
```bash
DATABASE_URL=your_database_url
OPENWEATHER_API_KEY=your_api_key
```

## Secrets and .env
The .env file may contain passwords, API keys, and other sensitive information.

**Do not commit the .env file to GitHub.**

Real API keys and database passwords must not be added to the source code or documentation.

A .env.example file can be committed if it contains only example or placeholder values.

For example:
``` bash
DATABASE_URL=your_database_url
OPENWEATHER_API_KEY=your_api_key
```

## Local runs
For a local run, make sure the required values are available in the .env file.

The CLI reads the configuration and passes the required values to the pipeline runner.

Example:
```bash
PYTHONPATH=services/pipeline/src python -m pipeline.cli --start "2026-08-20 00:00" --end "2026-08-23 00:00"
```

## Scheduled runs

The City Air Tracker scheduler uses Prefect to run shared pipeline on a cron schedule.

Required environment variables:

- DATABASE_URL - PostgreSQL connection.
- OPENWEATHER_API_KEY - OpenWeather API key.
- PIPELINE_SCHEDULE_CRON - schedule for the pipeline
- PIPELINE_HISTORY_HOURS - historical data window

The optional CITIES_CSV_FILE variable can be used to specify the path to the city input CSV file. If it is not set, the scheduler uses: 
```text
services/pipeline/config/cities.csv
```

For local scheduled runs, configure these variables in the local `.env` file . API keys and database credentials must not be committed to the repository.

Run locally:

Start Prefect:
```bash
.venv/bin/prefect server start
```

Then start the scheduler:

```bash
PREFECT_API_URL=http://127.0.0.1:4200/api \
PYTHONPATH=services/pipeline/src \
.venv/bin/python -m pipeline.scheduler
```
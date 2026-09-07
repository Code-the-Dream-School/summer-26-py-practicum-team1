# Final Project Documentation

## 1. Project Overview 

City Air Tracker is a web application that allows users to view air quality data for different cities.

The project collects air pollution data from the OpenWeather API, transforms the data into our project format, stores the data in PostgreSQL, and prepares the data for the dashboard.

The  main goal of the project is to make air quality data easier to view and understand.

## 2. Data Flow

The project follows this data flow:

City
-> Geocoding
-> OpenWeather API
-> Transform & Validate
-> PostgreSQL
-> Data-serving layer 
-> Dashboard

First, the city is geocoded to get its latitude and longitude.

The pipeline then uses the OpenWeather Air Pollution API to collect air quality data.

We save the raw API response in PostgreSQL for traceability and debugging. 

Then we transform and validate the data and store the processed data in PostgreSQL in our project format.

Finally, the data-serving layer queries PostgreSQL and prepares the data for the dashboard.

The dashboard then displays the air quality data to users.

## 3. What We Built

The project includes:

- A pipeline for collecting air quality data.
- City geocoding to get latitude and longitude.
- OpenWeather API integration for extracting air quality data.
- Raw API response storage in PostgreSQL for traceability and debugging.
- Data transformation and validation.
- PostgreSQL database storage for processed air quality data.
- Parquet export  of transformed records as a secondary output.
- Alembic database migration
- Database upsert behavior to prevent duplicate records.
- Pipeline run tracking for status, start and end times, processed records, and errors.
- A shared pipeline runner that coordinates the ETL process.
- Runtime logging for pipeline stages, successes, and failures.
- A manual CLI entrypoint for triggering the pipeline.
- A scheduled pipeline runner using Prefect.
- Runtime configuration and environment variable documentation.
- A data-serving layer for the dashboard.
- A React/Vite dashboard for displaying air quality information.
- End-to-end verification from the pipeline to the dashboard.

The project supports two ways to trigger the pipeline:

1. **Manual execution through the CLI.**
2. **Scheduled execution through Prefect.**

Both trigger the same shared pipeline runner, so the ETL logic is not duplicated.

## 4. Unfinished Work and Out of Scope 

The required functionality for the local project walkthrough has been implemented.

The project focuses on demonstrating the complete local workflow from data extraction through data storage and dashboard display.

Cloud deployment and production hosting are outside the scope of the current project.

## 5. Local Runtime Configuration

The project can be run locally for development and demonstration.

### Environment Variables 

The pipeline uses the following environment variables:

- `DATABASE_URL` - PostgreSQL database connection URL.
- `OPENWEATHER_API_KEY` - API key used to access the OpenWeather API.
- `PIPELINE_SCHEDULE_CRON` - cron schedule for scheduled pipeline runs.
- `PIPELINE_HISTORY_HOURS` - number of hours of historical data to retrieve.
- `CITIES_CSV_FILE` - path to the city input CSV file.
- `PARQUET _EXPORT_DIR` - directory where transformed Parquet files are exported. The default ia data/export.

For local development, these values should be provided through a `.env` file.

Example:

```dotenv
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5433/air_tracker
OPENWEATHER_API_KEY=your_api_key
PIPELINE_SCHEDULE_CRON='0 * * * *'
PIPELINE_HISTORY_HOURS=24
CITIES_CSV_FILE=services/pipeline/config/cities.csv
```

PARQUET_EXPORT_DIR is optional. If it is not provided, the project uses:

```dotenv
data/exports
```

**Secrets**

The .env file may cintain sensitive information such as API keys and database passwords.

The .env file must not be committed to GitHub.

Real API keys and database passwords must not be added to source code or documentation.

A .env.example file can be committed with placeholder values.

**Database**

PostgreSQL is used as the project's database.

For local development, PostgreSQL runs in Docker.

The local PostgreSQL configuration is :

- Database: air_tracker
- Username: postgres
- Password: postgres 
- Host: localhost
- PostgreSQL host port: 5433
- PostgreSQL container port: 5432

Start PostgreSQL with:

```dotenv 
docker compose up -d postgres
```
Stop PostgreSQL with:

```dotenv
docker compose down
```

Alembic is used to manage database dchema migrations.

Apply the migration with:

```dotenv
alembic upgrade head
```

**Ports**

The local project uses the following ports:

| Service | Port |
| --- | --- |
|PostgreSQL | 5433 |
| Flask Data API | 5000 |
| React/Vite Dashboard | 5173 |
| Prefect UI | 4200 |

The React/Vite dashboard proxies / api requests to the Flask Data API running on localhost:5000.

## 6. Local Walkthrough / Demo Runbook

The following steps describe how to run the project locally from a pipeline run to the dashboard.

**Prerequisites**

Before starting the walkthrough, make sure you have:

- Docker and Docker Compose installed.
- Python environment and project dependencies installed.
- Node.js and npm installed.
- A valid OpenWeather API key.
- A local .env file with the required configuration.

**Step 1: Start PostgreSQL**

From the project root, start the PostgreSQL container:

```dotenv
docker compose up -d postgres 
```

The database will be available on:

```dotenv
localhost:5433
```

**Step 2: Apply Database Migrations**

From the project root, run:
 
```dotenv
alembic upgrade head 
```

This creates the required PostgreSQL tables.

**Step 3: Trigger a Manual Pipeline Run**

The pipeline can be triggered manually through the CLI.

For example:

```bash 
PYTHONPATH=services/pipeline/src python -m pipeline.cli --start "2026-08-20 00:00" --end "2026-08-23 00:00"
```

The pipeline performs the following steps:

1. Reads the configured cities.
2. Validates the location input.
3. Geocodes cities when coordinates are needed.
4. Requests air quality data from the OpenWeather API.
5. Stores the raw API response in PostgreSQL.
5. Transforms and validates the raw data.
7. Upserts the processed observations into PostgreSQL.
8. Exports transformed records to Parquet.
9. Records the pipeline run status, timing, record count, and errors.

The CLI reports whether the pipeline run succeeded  or failed.

**Step 4: Verify the Pipeline Run**

Pipeline execution information is stored in the pipeline_runs table.

A successful run should have a status of :
```bash 
success
```

**Step 5: Start the Flask Data APi**

From the project root, start the dashboard data-serving layer:

```bash 
PYTHONPATH=. python -m services.dashboard.server
```
The API runs on:

```bash
http://localhost:5000
```
The main endpoints are:
```bash
GET /api/locations
GET /api/locations/<location_id>/observations
```
The API reads processed air quality data from PostgreSQL and returns the data needed by the dashboard.

**Step 6: Start the React Dashboard**

Open a new terminal and go to the frontend directory:

```
cd services/dashboard/frontend
```
Install the frontend dependencies:

```
npm install
```

Start the development server:

``` 
npm run dev
```

The dashboard will be available at:

```
http://localhost:5173
```

**Step 7: What the Audience Should See**

During the final walkthrough, the audience should be able to see the complete flow:

Pipeline Run -> OpenWeather API -> Transform & Validate -> PostgreSQL -> Flask Data API -> React Dashboard

On the dashboard, the audience should be able to:

- Select a city.
- View the latest air quality information.
- View the AQI status.
- View the PM2.5 measurements.
- View the PM10 measurements.
- View the ozone measurements.
- View historical air quality trends.
- View the selected city's country and coordinates.
- View the latest observation timestamp.

The dashboard also handles common states such as loading, errors, and no available data.

## 7. Scheduled Pipeline with Prefect

In addition to the manual CLI, the project supports scheduled pipeline execution usin Prefect.

Start the local Prefect server:

```bash 
.venv/bin/prefect server start 
```
The Prefect UI is available at:

```
http://127.0.0.1:4200
```

Start the scheduled pipeline from the project root:


```bash
PREFECT_API_URL=http://127.0.0.1:4200/api \
PYTHONPATH=services/pipeline/src \
.venv/bin/python -m pipeline.scheduler
```

The scheduler uses:

- PIPELINE_SCHEDULE_CRON to determine when the pipeline runs.
- PIPELINE_HISTORY_HOURS to determine the rolling historical data window.

The scheduler calls the same shared pipeline runner used by the manual CLI.

A successful scheduled run is shown as successful in Prefect and records the corresponding pipeline run in PostgreSQL.

## 8. Expected Demo Result 

The final local demonstration shows the complete end-to-end workflow:

City Configuration -> Geocoding -> OpenWeather API -> Extract -> Transform & Validate -> PostgreSQL -> Flask Data API -> React Dashboard 

The pipeline also produces a secondary Parquet output.

The final result is an interactive dashboard where users can select a city and view its air quality data and historical trends.

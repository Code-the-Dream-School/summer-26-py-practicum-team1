# Database Schema

## Locations

Stores location information used for air quality observations.

| Column       | Type             | Required | Description              |
| ------------ | ---------------- | -------- | ------------------------ |
| id           | BIGSERIAL        | Yes      | Primary key              |
| city         | TEXT             | Yes      | City name                |
| country_code | CHAR(2)          | Yes      | Two-letter country code  |
| state        | TEXT             | No       | Optional state or region |
| latitude     | DOUBLE PRECISION | Yes      | Location latitude        |
| longitude    | DOUBLE PRECISION | Yes      | Location longitude       |

### Constraints

- Primary key: `id`
- Unique: `city`, `country_code`, `latitude`, `longitude`

## Air Quality Records

Stores transformed air quality observations for each location.

| Column      | Type             | Required | Description                            |
| ----------- | ---------------- | -------- | -------------------------------------- |
| id          | BIGSERIAL        | Yes      | Primary key                            |
| location_id | BIGINT           | Yes      | References the location                |
| observed_at | TIMESTAMPTZ      | Yes      | Time when the observation was recorded |
| aqi         | SMALLINT         | Yes      | Air Quality Index from 1 to 5          |
| pm2_5       | DOUBLE PRECISION | No       | PM2.5 concentration                    |
| pm10        | DOUBLE PRECISION | No       | PM10 concentration                     |
| no2         | DOUBLE PRECISION | No       | Nitrogen dioxide concentration         |
| o3          | DOUBLE PRECISION | No       | Ozone concentration                    |

### Constraints

- Primary key: `id`
- Foreign key: `location_id` references `locations(id)`
- Unique: `location_id`, `observed_at`

## Pipeline Runs

Stores information about each pipeline execution.

| Column            | Type        | Required | Description                                |
| ----------------- | ----------- | -------- | ------------------------------------------ |
| id                | BIGSERIAL   | Yes      | Primary key                                |
| started_at        | TIMESTAMPTZ | Yes      | Time when the pipeline run started         |
| finished_at       | TIMESTAMPTZ | No       | Time when the pipeline run finished        |
| status            | TEXT        | Yes      | Current status of the pipeline run         |
| records_processed | INTEGER     | Yes      | Number of records processed during the run |
| error_message     | TEXT        | No       | Error details if the pipeline run failed   |

### Constraints

- Primary key: `id`

## Relationships

- One location can have many air quality records.
- Each air quality record belongs to one location.
- `air_quality_records.location_id` references `locations.id`.
- `pipeline_runs` is stored separately for pipeline execution tracking.

## Design Decisions

- PostgreSQL is the target database for Sprint 4.
- Raw OpenWeather API responses are not stored in the database for the MVP.
- Raw responses can be logged when needed for debugging.
- Transformed air quality records are persisted in PostgreSQL.
- One air quality record is allowed per location and observation timestamp.

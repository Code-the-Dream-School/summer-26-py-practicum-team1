# Local PostgreSQL and Alembic Migration Workflow
This project uses PostgreSQL  in Docker and Alembic for database migrations.

## 1. Start PostgreSQL
Make sure Docker Desktop is runnung.

From the project root, run:

```bash
docker compose up -d
```
Check that the PostgreSQL container is running:
```bash
docker compose ps
```
The container should show as Up.

## 2. Activate the virtual environment
Before running Alembic commands, activate the project's virtual environment.

On macOS/Linux:
```bash
source ./venv/bin/activate
```
On Windows/Git Bash:
```bash
source ./venv/Scripts/activate
```

## 3. Configure the database connection
Create a local .env file in the project root:

DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5433/air_tracker

This connects the application and Alembic to the PostgreSQL database running in Docker.

Make sure the .env file is in the project root before running Alembic commands.

## 4. Apply the database migration

After PostgreSQL is running and the virtual environment is activated, apply the database schema with:

```bash
alembic upgrade head
```
This creates the database tables automatically. No tables need to be created manually.

To check which migration is currently applied, run:
```bash
alembic current
```
The current migration should show the latest migration as head.

## 5. Database tables
The initial migration creates the following tables:

* locations - stores city and location information.
* air_quality_records - stores air quality measurements.
* pipeline_runs - stores information about pipeline runs.

The migration also creates the required foreign keys, unique constraints, and check constraints.

## 6. Create a new migration
When the SQLAlchemy models are changed , create a new migration with:
```bash
alembic revision --autogenerate -m "describe your change"
```
Review the generated migration file before applying it.

Then apply the migration:
```bash 
alembic upgrade head 
```

## 7. Roll back the latest migration
If needed, the latest migration can be rolled back with:
```bash 
alembic downgrade -1
```

## 8. Starting from an empty database
A teammate can start with an empty PostgreSQL database and build the schema without manually creating tables.

**The workflow is:**

 Start Docker PostgreSQL
        ↓ 
 Activate the virtual environment 
        ↓ 
 Create the .env file 
        ↓ 
 Run alembic upgrade head 
        ↓ 
 Database schema is created


PostgreSQL runs locally in Docker. The host port is 5433 because port 5432 is already used by another PostgreSQL installation.
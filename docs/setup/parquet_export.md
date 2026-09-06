# Parquet Export

City Air Tracker supports an optional local Parquet export of
transformed air-quality records.

## Storage priority

PostgreSQL remains the primary storage path.

Parquet export is a secondary output and runs after transformed
records have been successfully written to PostgreSQL.

A Parquet export failure is logged and does not roll back or remove
data already written through the PostgreSQL path.

## Export location

By default, files are written to:

`data/exports/`

The output directory can be changed with:

`PARQUET_EXPORT_DIR`

Example:

`PARQUET_EXPORT_DIR=data/archive`

## File naming

Files are associated with a pipeline run.

Example:

`new_york_run_42.parquet`

## Empty results

If transformation returns no records, no Parquet file is created.
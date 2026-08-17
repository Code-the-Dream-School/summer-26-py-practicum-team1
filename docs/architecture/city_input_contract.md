# City Input Contract

## Purpose

The city input contract defines the required structure for city configuration data used by the City Air Tracker pipeline.

The city configuration provides the list of locations processed by the extract layer.

The extract layer validates each configured location, uses the OpenWeather Geocoding API to resolve latitude and longitude, and then retrieves air pollution data from the OpenWeather Air Pollution API.

The pipeline uses this information to:

- identify target locations,
- resolve coordinates through geocoding,
- retrieve OpenWeather air pollution data,
- associate collected measurements with a city and country.

## Required Fields

The city input must contain the following fields:

| Field         | Type   | Required | Description                                        |
|---------------|--------|----------|----------------------------------------------------|
| city          | string | Yes      | City name used for geocoding and display           |
| country_code  | string | Yes      | ISO country code used for reliable location lookup |
| state         | string | No       | Optional state or region identifier                |

## Missing or Invalid Values

- If `city` is missing, the record is rejected.
- If `country_code` is missing, the record is rejected because reliable geocoding is not possible.
- If `state` is missing, processing continues because the field is optional.
- Empty rows are ignored.
- Invalid records are skipped, and validation errors are logged or clearly reported.
- Processing continues for the remaining valid records.

## Current Input Format

The current implementation uses a CSV file for city configuration.

## Processing

The extract layer processes the location input as follows:

1. Read the configured CSV file.
2. Parse each row into a Python dictionary.
3. Validate the required fields.
4. Skip invalid records and report validation errors.
5. Resolve coordinates using the OpenWeather Geocoding API.
6. Pass the coordinates to the OpenWeather Air Pollution API.

## Input File Location

The city configuration is stored in the CSV file specified by the `CITIES_CSV_FILE` environment variable.

If `CITIES_CSV_FILE` is not set, the default location is:

```text
services/pipeline/config/cities.csv
```

The extract layer reads this file as the source of location records.

## Python Representation

Each valid location record is returned as a Python dictionary.

```python
{
    "city": "Charlotte",
    "country_code": "US",
    "state": "NC"
}
```

## Valid Example

CSV columns example:

```csv
city,country_code,state
Charlotte,US,NC
Vancouver,CA,
London,GB,
Melbourne,AU,VIC
Paris,FR,
```
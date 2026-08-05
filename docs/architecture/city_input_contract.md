# City Input Contract

## Purpose

The city input contract defines the required structure for city configuration data used by the City Air Tracker pipeline.

The city configuration provides the list of cities that the extract stage processes. The pipeline uses this information to:
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

## Current Input Format

The current implementation uses a CSV file for city configuration.

## Valid Example

CSV columns example:

city,country_code,state
Charlotte,US,NC
Vancouver,CA,
London,GB,
Melbourne,AU,VIC
Paris,FR,
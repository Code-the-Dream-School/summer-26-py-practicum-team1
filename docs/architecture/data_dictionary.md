# Data Dictionary

This document describes the fields in the clean data output.

| Field name | Description | Data type | Unit/Format | Source/Transformation | Required |
|---|---|---|---|---|---|
| location | Location associated with the observation | string | {city}, {country_code}, with {state} only when state is present | Created from the original location context | Yes |
| latitude | Latitude of the observed location | float | Decimal degrees | Copied from coord.lat | Yes |
| longitude | Longitude of the observed location | float | Decimal degrees | Copied from coord.lon | Yes |
| observed_at | Date and time when the air-quality observation was recorded | datetime | ISO 8601 UTC; timezone-aware datetime | list[].dt converted from Unix seconds to UTC datetime | Yes |
| aqi | OpenWeather air quality index category | integer | 1-5 | Copied from list[].main.aqi | Yes |
| pm2_5 | Fine particulate matter concentration | float | µg/m³ | Copied from list[].components.pm2_5 | Optional |
| pm10 | Particulate matter concentration | float | µg/m³ | Copied from list[].components.pm10 | Optional |
| no2 | Nitrogen dioxide concentration | float | µg/m³ | Copied from list[].components.no2 | Optional |
| o3 | Ozone concentration | float | µg/m³ | Copied from list[].components.o3 | Optional |
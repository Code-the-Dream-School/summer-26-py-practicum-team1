# OpenWeather Air Pollution Normalization Rules

## Purpose

This document defines the normalization contract between the raw OpenWeather Air Pollution response and the normalized records produced by the pipeline transform layer.

It specifies how raw API fields are converted into the canonical record format consumed by downstream pipeline components.

For the raw API payload definition, see `raw_response_contract.md`.
For the location input contract, see `city_input_contract.md`.

---

## Output Record Granularity

One normalized output record represents one observation for one location at one timestamp.

A single OpenWeather response may therefore produce multiple normalized records, one for each item in the `list[]` array.

---

## Normalization Rules

| Source field | Output field | Required | Normalization rule | Missing value behavior |
| --- | --- | :---: | --- | --- |
| Request location (`city`, `country_code`, optional `state`) | `location` | Yes | Preserve the requested location as the normalized location identifier. Format: `city, country_code` or `city, country_code, state` when a state is present. | Missing or invalid required location fields prevent records from being created for the payload. |
| `coord.lat` | `latitude` | Yes | Normalize to `float` and rename to `latitude`. | Invalid or missing values prevent records from being created. |
| `coord.lon` | `longitude` | Yes | Normalize to `float` and rename to `longitude`. | Invalid or missing values prevent records from being created. |
| `list[].dt` | `observed_at` | Yes | Convert the Unix timestamp to a timezone-aware UTC `datetime`. | Invalid observations are skipped. |
| `list[].main.aqi` | `aqi` | Yes | Preserve the OpenWeather AQI category after validating that it is within the supported range (1–5). | Invalid observations are skipped. |
| `list[].components.pm2_5` | `pm2_5` | No | Copy the pollutant concentration as `float`. | Missing or invalid values become `None`. |
| `list[].components.pm10` | `pm10` | No | Copy the pollutant concentration as `float`. | Missing or invalid values become `None`. |
| `list[].components.no2` | `no2` | No | Copy the pollutant concentration as `float`. | Missing or invalid values become `None`. |
| `list[].components.o3` | `o3` | No | Copy the pollutant concentration as `float`. | Missing or invalid values become `None`. |

---

## Normalization Behavior

The transform layer follows these rules:

- Each observation is normalized independently.
- Invalid required observation fields (`dt` or AQI) cause only the corresponding observation to be skipped. Invalid location context or coordinates prevent records from being created for the payload.
- Later valid observations in the same payload continue to be processed.
- Missing optional pollutant values do not prevent record creation and are normalized to `None`.
- The normalized schema intentionally contains only the fields required by downstream storage and dashboard components.

---

## Related Documents

- `raw_response_contract.md` — structure of the raw OpenWeather response.
- `city_input_contract.md` — location input contract.
- `api_extraction_strategy.md` — API retrieval strategy.

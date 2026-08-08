# API Direction and Extraction Plan (Sprint 2 / SCRUM-17)

## Purpose and Decision Status

This document defines the MVP direction for resolving configured cities and extracting historical air-pollution data. It is a lightweight API decision artifact, not an implementation design or database schema.

**Selected primary MVP provider:** OpenWeather.

OpenWeather was selected because the existing project flow, city input contract, product summary, and API field reference already assume OpenWeather geocoding and historical air-pollution data. Using a single provider keeps the MVP extraction path and response contract focused.

---

## MVP Extraction Flow

```text
city configuration
  -> OpenWeather geocoding
  -> latitude/longitude
  -> OpenWeather historical air pollution
  -> full raw response
  -> transform/load
  -> dashboard
```

---

## Selected API Endpoints

### 1. Direct Geocoding

Documentation: [OpenWeather Geocoding API](https://openweathermap.org/api/geocoding-api)

Endpoint:

`GET https://api.openweathermap.org/geo/1.0/direct`

Required request parameters:

| Parameter | Source | Notes |
|---|---|---|
| `q` | City input contract | Location query assembled from `city`, optional `state`, and `country_code` |
| `appid` | Environment configuration | OpenWeather API key |

Optional request parameter:

| Parameter | MVP use |
|---|---|
| `limit` | Limit candidate results so ambiguous locations can be handled explicitly |

The location query is constructed as:

```text
city,state,country_code
```

If `state` is absent, the query becomes:

```text
city,country_code
```

For example, if the CSV contract stores:

```text
Charlotte,US,NC
```

where the columns represent:

```text
city,country_code,state
```

the extractor should construct the OpenWeather query as:

```text
Charlotte,NC,US
```

The selected geocoding result supplies `lat` and `lon`. The result should also be validated against the requested city, country code, and optional state before extraction continues.

---

### 2. Historical Air Pollution

Documentation: [OpenWeather Air Pollution API](https://openweathermap.org/api/air-pollution)

Endpoint:

`GET https://api.openweathermap.org/data/2.5/air_pollution/history`

Required request parameters:

| Parameter | Source | Notes |
|---|---|---|
| `lat` | Selected geocoding result | Latitude of the resolved city |
| `lon` | Selected geocoding result | Longitude of the resolved city |
| `start` | Runtime configuration | Start of the historical range as Unix seconds (UTC) |
| `end` | Runtime configuration | End of the historical range as Unix seconds (UTC) |
| `appid` | Environment configuration | OpenWeather API key |

The extractor should validate that `start <= end` before making the request.

---

## API Key Handling

The OpenWeather API key must be supplied through environment configuration and must never be:

- hardcoded,
- committed to version control,
- included in documentation examples,
- written to logs.

Documentation and sample configuration should use a placeholder such as:

```text
OPENWEATHER_API_KEY
```

instead of a real secret.

---

## MVP Response Fields

The transform stage is expected to prioritize these historical-response fields:

| Response field | MVP use |
|---|---|
| `list[].dt` | Observation timestamp in Unix seconds (UTC) |
| `list[].main.aqi` | OpenWeather AQI category (1 through 5) |
| `list[].components.pm2_5` | PM2.5 concentration |
| `list[].components.pm10` | PM10 concentration |
| `list[].components.no2` | Nitrogen dioxide concentration |
| `list[].components.o3` | Ozone concentration |

The complete field definitions and units remain in the [OpenWeather Environmental API Field Reference](../reference/openweather_environmental_api_fields_reference.md); they are intentionally not duplicated here.

The full raw API response should be preserved for traceability and reproducibility even when only selected fields are used downstream.

This decision does not define the persistence mechanism, database, table, or schema.

---

## Common Extraction Concerns

- **Invalid locations:** Reject city records that lack required `city` or `country_code` values before making a request.
- **Ambiguous locations:** Do not silently accept an unrelated first result; compare candidates with the requested city, country code, and optional state.
- **Authentication errors:** Stop the affected extraction, report a clear error, and never expose the API key.
- **Rate limiting and usage limits:** Detect rate-limit responses and use a bounded retry/backoff policy when extraction is implemented. Request volume must remain within the limits of the team's OpenWeather subscription plan; the applicable limits should be confirmed before implementation.
- **Empty responses:** Treat an empty geocoding candidate list or an empty pollution `list` as an explicit no-data result, not a successful populated extract.
- **Malformed responses:** Validate the expected response shape before passing data downstream and preserve useful error context without exposing secrets.
- **Network failures:** Treat timeouts and connection errors as retryable only within a bounded retry policy.
- **Invalid historical ranges:** Validate UTC Unix timestamps and require `start <= end` before calling the history endpoint.

---

## Trimmed Historical Response Example

```json
{
  "coord": [50.0, 50.0],
  "list": [
    {
      "dt": 1606482000,
      "main": {
        "aqi": 2
      },
      "components": {
        "pm2_5": 13.448,
        "pm10": 15.524,
        "no2": 43.184,
        "o3": 4.783
      }
    }
  ]
}
```

---

## Alternatives Considered

### Open-Meteo

Open-Meteo was considered as an alternative provider. It is not proposed for the MVP because adding a second provider would introduce another request contract, response mapping, and failure path before the initial extraction flow is established.

It can be revisited if the team identifies a requirement that OpenWeather does not meet.

---

## MVP vs Future Scope

### MVP

- Use OpenWeather as the primary provider.
- Resolve configured cities through the OpenWeather Direct Geocoding API.
- Request historical air-pollution data through the OpenWeather Historical Air Pollution API.
- Preserve the complete raw API response for traceability and reproducibility.
- Prioritize timestamp, AQI, PM2.5, PM10, NO2, and O3 downstream.

### Future Scope

- Current air-pollution endpoint.
- Air-pollution forecast endpoint.
- Open-Meteo or other additional/fallback providers.
- Provider abstraction.
- Provider failover.
- Cross-provider comparison.

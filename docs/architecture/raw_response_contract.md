## Raw Response Contract
### Request Context

- **Source location:** City records are read  from `CITIES_CSV_FILE`; default: `services/pipeline/config/cities.csv`

- **API:** OpenWeather

### Direct Geocoding API
**Purpose:**  Resolve configured city locations to latitude and longitude

**Endpoint:** 
`GET https://api.openweathermap.org/geo/1.0/direct`

### Historical Air Pollution API

**Purpose:** Retrieve historical air-pollution measurements for the resolved coordinates.

**Endpoint:**
`GET https://api.openweathermap.org/data/2.5/air_pollution/history`

- **Historical window:** start=1606488670, end=1606747870 (UTC)
- **Response retrieved at:** Not included in the OpenWeather raw response.

### Raw OpenWeather Payload
```json
{
  "coord": {
    "lon": 50,
    "lat": 50
  },
  "list": [
    {
      "main": {
        "aqi": 1
      },
      "components": {
        "co": 226.97,
        "no": 0,
        "no2": 2.29,
        "o3": 46.49,
        "so2": 0.95,
        "pm2_5": 0.9,
        "pm10": 0.93,
        "nh3": 0.09
      },
      "dt": 1606489200
    },
    {
      "main": {
        "aqi": 1
      },
      "components": {
        "co": 226.97,
        "no": 0,
        "no2": 2.21,
        "o3": 43.27,
        "so2": 0.92,
        "pm2_5": 0.87,
        "pm10": 0.91,
        "nh3": 0.09
      },
      "dt": 1606492800
    },
    {
      "main": {
        "aqi": 1
      },
      "components": {
        "co": 230.31,
        "no": 0,
        "no2": 2.4,
        "o3": 38.27,
        "so2": 0.86,
        "pm2_5": 0.78,
        "pm10": 0.8,
        "nh3": 0.08
      },
      "dt": 1606496400
    }
  ]
}
```

Sample shown with three observations from the requested historical window. The actual API response contains additional observations.


### Important Response Fields

The following fields are prioritized for downstream processing and dashboard use:

| Field | Purpose |
|---|---|
| `list[].dt` | Observation timestamp |
| `list[].main.aqi` | Air quality index |
| `list[].components.pm2_5` | PM2.5 concentration |
| `list[].components.pm10` | PM10 concentration |
| `list[].components.no2` | Nitrogen dioxide concentration |
| `list[].components.o3` | Ozone concentration |

The complete raw API response should be preserved for traceability and reproducibility.



### Sprint 3 Handoff 

The storage layer should be able to accept the raw OpenWeather Air Pollution API response together with the source location and response metadata.

The storage layer will need to preserve:
- the source location;
- the API response;
- observation timestamps;
- the air-quality and pollutant fields identified above;
- request/response context needed for traceability.

Questions remaining for Sprint 3:

- How should the raw response be stored?
- What database/table structure should be used?
- What information should be stored for each location and observation?
# Transform input and output contract

## 1. Transform Input - What it receives

*Expected raw payload:*

A raw response from the OpenWeather Historical Air Pollution API.

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
    }
  ]
}
``` 

*Location context:* The transform receives the original city input from the extraction step: city and country code are required, while state is optional.

Example:

city: Raleigh

country_code: US

state: NC

If state is not provided, the transform can still process the location.

Example:

city: Paris
country_code: FR
state: None

## Transform Contract

Conceptually, the transform receives the raw OpenWeather payload and the location context and returns a list of clean records:

transform(raw_payload, location_context) -> list[CleanRecord]

## 2. Output Record Granularity

**One clean record = one location at one timestamp**

Example:

Raleigh 10:00 -> record 1
Raleigh 11:00 -> record 2
Raleigh 12:00 -> record 3


## 3. Raw-to-Clean Field Mapping
The transform only maps the fields explicitly defined in this contract. Additional fields returned by OpenWeather (for example, new fields added to components) are ignored unless they are added to the clean output contract in a future update.

| Raw field | Clean field | Transformation | Required |
|---|---|---|---| 
| `location_context.city, location_context.country_code, location_context.state` | location | Combined into a location label; state is omitted when not provided | Yes |
| `coord.lat` | latitude | Copied from raw response | Yes |
| `coord.lon` | longitude | Copied from raw response | Yes |
| `list[].dt` | observed_at | Converted from Unix seconds to UTC datetime | Yes |
| `list[].main.aqi` | aqi | Copied from raw response | Yes |
| `list[].components.pm2_5` | pm2_5 | Copied from raw response | No |
| `list[].components.pm10` | pm10 | Copied from raw response | No |
| `list[].components.no2` | no2 | Copied from raw response | No |
| `list[].components.o3` | o3 | Copied from raw response | No |

## 4. Example transformed record

Based on the proposed transorm contract and the Sprint 2 sample payload, one clean record would look like this:

```json
{
  "location": "Example City, US, NC",
  "latitude": 50,
  "longitude": 50,
  "observed_at": "2020-11-27T07:00:00Z",
  "aqi": 1, 
  "pm2_5": 0.9,
  "pm10": 0.93,
  "no2": 2.29,
  "o3": 46.49
}
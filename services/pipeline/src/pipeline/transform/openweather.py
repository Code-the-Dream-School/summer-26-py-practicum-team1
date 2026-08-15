import logging
import math
from datetime import datetime, timezone


logger = logging.getLogger(__name__)

POLLUTANT_FIELDS = (
    "co",
    "no",
    "no2",
    "o3",
    "so2",
    "pm2_5",
    "pm10",
    "nh3",
)


def _log_invalid(field, value):
    logger.warning("Invalid or missing normalization value: field=%s value=%r", field, value)


def _normalize_number(value, field):
    if value is None or isinstance(value, bool):
        _log_invalid(field, value)
        return None

    try:
        normalized = float(value)
    except (TypeError, ValueError):
        _log_invalid(field, value)
        return None

    if not math.isfinite(normalized):
        _log_invalid(field, value)
        return None

    return normalized


def _normalize_timestamp(value, field):
    normalized = _normalize_number(value, field)

    if normalized is None:
        return None

    if not normalized.is_integer():
        _log_invalid(field, value)
        return None

    try:
        return datetime.fromtimestamp(normalized, tz=timezone.utc)
    except (OverflowError, OSError, ValueError):
        _log_invalid(field, value)
        return None


def _normalize_aqi(value, field):
    normalized = _normalize_number(value, field)

    if normalized is None:
        return None

    if not normalized.is_integer():
        _log_invalid(field, value)
        return None

    normalized = int(normalized)

    if normalized not in range(1, 6):
        _log_invalid(field, value)
        return None

    return normalized


def _format_location(location):
    if not isinstance(location, dict):
        _log_invalid("location", location)
        return None

    city = location.get("city")
    country_code = location.get("country_code")
    state = location.get("state")

    if not isinstance(city, str) or not city.strip():
        _log_invalid("location.city", city)
        return None

    if not isinstance(country_code, str) or not country_code.strip():
        _log_invalid("location.country_code", country_code)
        return None

    if state is not None and not isinstance(state, str):
        _log_invalid("location.state", state)
        return None

    parts = [city.strip(), country_code.strip()]

    if state and state.strip():
        parts.append(state.strip())

    return ", ".join(parts)


def transform_air_pollution(raw_response, location):
    if not isinstance(raw_response, dict):
        _log_invalid("raw_response", raw_response)
        return []

    normalized_location = _format_location(location)
    coordinates = raw_response.get("coord")

    if not isinstance(coordinates, dict):
        _log_invalid("coord", coordinates)
        return []

    latitude = _normalize_number(coordinates.get("lat"), "coord.lat")
    longitude = _normalize_number(coordinates.get("lon"), "coord.lon")

    if normalized_location is None or latitude is None or longitude is None:
        return []

    observations = raw_response.get("list")

    if not isinstance(observations, list):
        _log_invalid("list", observations)
        return []

    records = []

    for index, item in enumerate(observations):
        if not isinstance(item, dict):
            _log_invalid(f"list[{index}]", item)
            continue

        observed_at = _normalize_timestamp(item.get("dt"), f"list[{index}].dt")
        main = item.get("main")

        if not isinstance(main, dict):
            _log_invalid(f"list[{index}].main", main)
            continue

        aqi = _normalize_aqi(main.get("aqi"), f"list[{index}].main.aqi")

        if observed_at is None or aqi is None:
            continue

        components = item.get("components")

        if not isinstance(components, dict):
            _log_invalid(f"list[{index}].components", components)
            components = {}

        normalized_components = {
            pollutant: _normalize_number(
                components.get(pollutant),
                f"list[{index}].components.{pollutant}",
            )
            for pollutant in POLLUTANT_FIELDS
        }

        records.append({
            "location": normalized_location,
            "latitude": latitude,
            "longitude": longitude,
            "observed_at": observed_at,
            "aqi": aqi,
            "pm2_5": normalized_components["pm2_5"],
            "pm10": normalized_components["pm10"],
            "no2": normalized_components["no2"],
            "o3": normalized_components["o3"],
        })

    return records

def prepare_air_quality_values(record):
    """Select transformed values stored in an air quality record row."""
    return {
        "observed_at": record["observed_at"],
        "aqi": record["aqi"],
        "pm2_5": record.get("pm2_5"),
        "pm10": record.get("pm10"),
        "no2": record.get("no2"),
        "o3": record.get("o3"),
    }

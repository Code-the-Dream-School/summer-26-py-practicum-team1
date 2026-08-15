def transform_air_pollution(raw_response, location):
  records = []

  for item in raw_response["list"]:
    record = {
      "location": ", ".join(
        part
        for part in [
          location["city"],
          location["country_code"],
          location.get("state"),
        ]
        if part
      ),
      "latitude": raw_response["coord"]["lat"],
      "longitude": raw_response["coord"]["lon"],
      "observed_at": item["dt"],
      "aqi": item["main"]["aqi"],
      "pm2_5": item["components"].get("pm2_5"),
      "pm10": item["components"].get("pm10"),
      "no2": item["components"].get("no2"),
      "o3": item["components"].get("o3"),
    }

    records.append(record)

  return records
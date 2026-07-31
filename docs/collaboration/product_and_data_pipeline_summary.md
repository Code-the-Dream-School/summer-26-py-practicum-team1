# Product and Data Pipeline Summary

## 1. Problem Statement 
City Air Tracker is designed to provide users with an easy way to monitor real-time air quality and analyze historical pollution trends for any city. 
Instead of dealing with complex environmental metrics, users can quickly look up a location and make informed decisions based on clear visual data.

## 2. Data Requirements
The application requires:
- Geographical coordinates (latitude and longitude) derived from city names using geocoding.
- Real-time and historical air pollution metrics (such as AQI and component concentrations like PM2.5, PM10, NO2) fetched from the OpenWeather API.
- Timestamps to track air quality changes over time.

## 3. ETL Pipeline Stages 
- **Extract**: Fetches raw air quality and location JSON payloads from the OpenWeather API endpoints.
- **Transform**: Parses and cleans the raw JSON responses, maps city names to coordinates, strips out unused metadata, and formats timestamps and numerical values for consistency.
- **Load**: Writes the processed, structured data into targeted tables within the PostgreSQL database.

## 4. Supporting the Dashboard
Once stored in PostgreSQL, the clean historical and current data is rapidly queried by the backend and served to the React dashboard. This enables the frontend to render real-time pollution stats and interactive historical charts seamlessly without relying on slow external API calls during user interactions.
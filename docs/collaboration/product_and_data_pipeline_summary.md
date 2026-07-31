# Product and Data Pipeline Summary

## 1. Problem Statement 
City Air Tracker is designed to provide users with an easy way to monitor and analyze historical pollution trends for any city. 
Instead of dealing with complex environmental metrics, users can quickly look up a location and make informed decisions based on clear visual data.

## 2. Data Requirements
The application requires:
- Geographical coordinates (latitude and longitude) derived from city names using geocoding.
- Historical air pollution metrics (such as AQI and component concentrations like PM2.5, PM10, NO2) fetched from the OpenWeather API.
- Timestamps to track air quality changes over time.

## 3. ETL Pipeline Stages 
- **Extract**: Fetches raw location and historical air pollution JSON payloads from the OpenWeather API endpoints and stores raw responses in PostgreSQL.
- **Transform**: Parses and cleans the payload, maps city names to coordinates, deduplicates entries, standardizes timestamps, and derives analytical metrics.
- **Load**: Saves the clean gold dataset, making it ready for analytics and visualization.

## 4. Supporting the Dashboard
The backend prepares the data in advance and serves it directly to the dashboard. This allows React to render charts instantly without waiting on slow third-party API responses.
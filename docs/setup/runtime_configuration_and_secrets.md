# Runtime Configuration and Secrets
The pipeline needs a few environment variables to run.

## Environment variables
The pipeline uses:
- DATABASE_URL - the connection URL for the PostgreSQL database
- OPENWEATHER_API_KEY - the API key used to access the OpenWeather API.

For local development, these values are stored in a .env file.

Example:
```bash
DATABASE_URL=your_database_url
OPENWEATHER_API_KEY=your_api_key
```

## Secrets and .env
The .env file may contain passwords, API keys, and other sensitive information.

**Do not commit the .env file to GitHub.**

Real API keys and database passwords must not be added to the source code or documentation.

A .env.example file can be committed if it contains only example or placeholder values.

For example:
``` bash
DATABASE_URL=your_database_url
OPENWEATHER_API_KEY=your_api_key
```

## Local runs
For a local run, make sure the required values are available in the .env file.

The CLI reads the configuration and passes the required values to the pipeline runner.

Example:
```bash
```

## Scheduled runs

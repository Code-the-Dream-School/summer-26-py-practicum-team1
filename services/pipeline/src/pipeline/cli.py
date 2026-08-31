import argparse
from datetime import datetime, timezone
from pipeline.extract.location_input import read_city_records
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", required=True)
    parser.add_argument("--end", required=True)

    args = parser.parse_args()

    load_dotenv()
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise RuntimeError("DATABASE_URL is not set")

    engine = create_engine(database_url)
    with engine.connect() as connection:
        print("Database connection successful")

    start = datetime.fromisoformat(args.start).replace(tzinfo=timezone.utc)
    end = datetime.fromisoformat(args.end).replace(tzinfo=timezone.utc)

    start_timestamp = int(start.timestamp())
    end_timestamp = int(end.timestamp())

    locations = read_city_records()

    print("Start:", start)
    print("End:", end)
    print("Start timestamp:", start_timestamp)
    print("End timestamp:", end_timestamp)
    print("Locations:", locations)
    print("Database URL:", database_url)

if __name__ == "__main__":
    main()

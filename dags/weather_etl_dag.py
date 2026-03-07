from datetime import datetime, timedelta
import os
import sys

sys.path.insert(0, '/opt/airflow')

from airflow.decorators import dag, task
from etl.extract   import extract_weather
from etl.transform import transform_weather
from etl.load      import load_weather

default_args = {
    "owner": "data-team",
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
    "email_on_failure": False,
}

@dag(
    dag_id="weather_etl_pipeline",
    description="ETL diario: Open-Meteo → PostgreSQL",
    schedule="@daily",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    default_args=default_args,
    tags=["etl", "weather", "portfolio"],
)
def weather_etl():
    """Pipeline ETL de datos meteorológicos usando Open-Meteo API."""

    @task()
    def extract() -> dict:
        lat = float(os.getenv("WEATHER_LAT", "19.4326"))
        lon = float(os.getenv("WEATHER_LON", "-99.1332"))
        return extract_weather(lat, lon)

    @task()
    def transform(raw: dict) -> list:
        city = os.getenv("WEATHER_CITY", "Ciudad de México")
        df = transform_weather(raw, city)
        # Convertir timestamps a string para que sean serializables
        df["timestamp"] = df["timestamp"].astype(str)
        df["extracted_at"] = df["extracted_at"].astype(str)
        return df.to_dict(orient="records")

    @task()
    def load(records: list) -> int:
        import pandas as pd
        df = pd.DataFrame(records)
        # Convertir strings de vuelta a datetime para PostgreSQL
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df["extracted_at"] = pd.to_datetime(df["extracted_at"])
        return load_weather(df)

    raw_data  = extract()
    clean_df  = transform(raw_data)
    load(clean_df)

weather_etl()
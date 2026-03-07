import os
import pandas as pd
import logging
from sqlalchemy import create_engine, text

logger = logging.getLogger(__name__)

def get_engine():
    """Crea engine de SQLAlchemy desde variables de entorno."""
    user = os.getenv("POSTGRES_USER")
    pwd  = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    db   = os.getenv("POSTGRES_DB")
    
    url = f"postgresql+psycopg2://{user}:{pwd}@{host}:{port}/{db}"
    return create_engine(url, pool_pre_ping=True)

def load_weather(df: pd.DataFrame) -> int:
    """
    Carga DataFrame en PostgreSQL con upsert (idempotente).
    
    Returns:
        Número de filas insertadas/actualizadas
    """
    engine = get_engine()
    
    # Staging table → upsert → producción
    with engine.begin() as conn:
        df.to_sql("weather_staging", conn,
                   if_exists="replace", index=False)
        
        upsert_sql = text("""
            INSERT INTO weather_hourly
                (city, timestamp, temperature_c, humidity_pct,
                 windspeed_kmh, feels_hot, extracted_at)
            SELECT city, timestamp, temperature_c, humidity_pct,
                   windspeed_kmh, feels_hot, extracted_at
            FROM weather_staging
            ON CONFLICT (city, timestamp)
            DO UPDATE SET
                temperature_c = EXCLUDED.temperature_c,
                humidity_pct  = EXCLUDED.humidity_pct,
                windspeed_kmh = EXCLUDED.windspeed_kmh,
                extracted_at  = EXCLUDED.extracted_at;
        """)
        result = conn.execute(upsert_sql)
    
    rows = result.rowcount
    logger.info(f"Cargadas {rows} filas en weather_hourly")
    return rows
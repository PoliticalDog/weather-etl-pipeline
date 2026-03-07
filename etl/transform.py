import pandas as pd
import logging

logger = logging.getLogger(__name__)

def transform_weather(raw_data: dict, city: str) -> pd.DataFrame:
    """
    Transforma datos crudos de la API en DataFrame normalizado.
    
    Args:
        raw_data: Respuesta JSON de la API
        city: Nombre de la ciudad para enriquecer el dataset
    
    Returns:
        DataFrame limpio y tipado listo para cargar
    """
    hourly = raw_data["hourly"]
    
    df = pd.DataFrame({
        "timestamp": hourly["time"],
        "temperature_c": hourly["temperature_2m"],
        "humidity_pct": hourly["relativehumidity_2m"],
        "windspeed_kmh": hourly["windspeed_10m"],
    })

    # Tipado correcto
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["city"] = city
    df["extracted_at"] = pd.Timestamp.now(tz="UTC")

    # Validación básica
    initial_rows = len(df)
    df = df.dropna(subset=["temperature_c", "humidity_pct"])
    df = df[df["temperature_c"].between(-50, 60)]
    df = df[df["humidity_pct"].between(0, 100)]

    dropped = initial_rows - len(df)
    if dropped > 0:
        logger.warning(f"Se descartaron {dropped} registros inválidos")

    # Feature derivada
    df["feels_hot"] = (
        (df["temperature_c"] > 28) & (df["humidity_pct"] > 60)
    )

    logger.info(f"Transform completado: {len(df)} filas")
    return df
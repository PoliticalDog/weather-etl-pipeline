import requests
import logging
from datetime import date

logger = logging.getLogger(__name__)

BASE_URL = "https://api.open-meteo.com/v1/forecast"

def extract_weather(lat: float, lon: float) -> dict:
    """
    Extrae datos meteorológicos de Open-Meteo API.
    
    Args:
        lat: Latitud de la ciudad
        lon: Longitud de la ciudad
    
    Returns:
        Dict con datos crudos de la API
    
    Raises:
        requests.HTTPError: Si la API responde con error
    """
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m,relativehumidity_2m,windspeed_10m",
        "timezone": "auto",
        "start_date": str(date.today()),
        "end_date": str(date.today()),
    }

    logger.info(f"Extrayendo datos: lat={lat}, lon={lon}")
    
    response = requests.get(BASE_URL, params=params, timeout=30)
    response.raise_for_status()
    
    data = response.json()
    logger.info(f"Datos recibidos: {len(data['hourly']['time'])} registros")
    
    return data
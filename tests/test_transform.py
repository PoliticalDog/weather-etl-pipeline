import pytest
from etl.transform import transform_weather

MOCK_API_RESPONSE = {
    "hourly": {
        "time": ["2024-01-01T00:00", "2024-01-01T01:00"],
        "temperature_2m": [22.5, 21.0],
        "relativehumidity_2m": [65, 70],
        "windspeed_10m": [12.3, 10.1],
    }
}

def test_transform_returns_dataframe():
    df = transform_weather(MOCK_API_RESPONSE, "Test City")
    assert len(df) == 2

def test_transform_columns():
    df = transform_weather(MOCK_API_RESPONSE, "Test City")
    expected = {"timestamp", "temperature_c", "humidity_pct",
                "windspeed_kmh", "city", "feels_hot", "extracted_at"}
    assert expected.issubset(df.columns)

def test_transform_city_column():
    df = transform_weather(MOCK_API_RESPONSE, "CDMX")
    assert (df["city"] == "CDMX").all()

def test_transform_drops_invalid_temp():
    bad_data = {"hourly": {
        "time": ["2024-01-01T00:00"],
        "temperature_2m": [999],   # temperatura inválida
        "relativehumidity_2m": [50],
        "windspeed_10m": [10],
    }}
    df = transform_weather(bad_data, "City")
    assert len(df) == 0
-- Creacion de tabla para almacenar datos meteorologicos horarios
CREATE TABLE IF NOT EXISTS weather_hourly (
    id          SERIAL PRIMARY KEY,
    city        VARCHAR(100) NOT NULL,
    timestamp   TIMESTAMPTZ  NOT NULL,
    temperature_c   NUMERIC(5,2),
    humidity_pct    SMALLINT,
    windspeed_kmh   NUMERIC(6,2),
    feels_hot       BOOLEAN,
    extracted_at    TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(city, timestamp)  -- evita duplicados
);

CREATE INDEX IF NOT EXISTS idx_weather_city_ts
    ON weather_hourly(city, timestamp DESC);
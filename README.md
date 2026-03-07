# Weather ETL Pipeline

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-2.9.0-017CEE?logo=apacheairflow)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker)
![Pandas](https://img.shields.io/badge/Pandas-2.2-150458?logo=pandas)

Pipeline ETL que extrae datos meteorológicos de la API Open-Meteo, los transforma con Python/Pandas, los carga en PostgreSQL y orquesta todo el flujo con Apache Airflow y Docker. Built as a portfolio project to demonstrate core Data Engineering skills: API ingestion, data transformation, relational storage, and workflow orchestration.

---

##  Arquitectura

```
Open-Meteo API
      │
      ▼
 [ Extract ]  ──  etl/extract.py   →  Consume la API con requests
      │
      ▼
 [ Transform ] ── etl/transform.py →  Limpia y valida con Pandas
      │
      ▼
 [ Load ]      ── etl/load.py      →  Upsert en PostgreSQL vía SQLAlchemy
      │
      ▼
 PostgreSQL (weather_hourly)

Todo orquestado por Apache Airflow (DAG diario) y contenedorizado con Docker Compose.
```

---

##  Stack Tecnológico

| Tecnología | Versión | Uso |
|---|---|---|
| Python | 3.11 | Lenguaje principal |
| Apache Airflow | 2.9.0 | Orquestación del pipeline |
| PostgreSQL | 15 | Base de datos destino |
| Pandas | 2.2 | Transformación de datos |
| SQLAlchemy | 2.0 | Conexión a PostgreSQL |
| Docker Compose | - | Contenedorización del entorno |
| Open-Meteo API | - | Fuente de datos (gratuita, sin API key) |

---

##  Estructura del Repositorio

```
weather-etl-pipeline/
├── dags/
│   └── weather_etl_dag.py       # DAG de Airflow (TaskFlow API)
├── etl/
│   ├── __init__.py
│   ├── extract.py               # Extracción desde Open-Meteo API
│   ├── transform.py             # Limpieza y validación con Pandas
│   └── load.py                  # Carga en PostgreSQL con upsert
├── sql/
│   └── create_tables.sql        # DDL: tabla weather_hourly
├── tests/
│   └── test_transform.py        # Tests unitarios con pytest
├── docs/
│   └── Dag_airflow.png                      # Captura airflow despliegue
│   └── Dag_etl_airflow_monitoring.png       # Captura flujo dag etl
│   └── pgAdmin_load_weather_hourly.png      # Captura datos cargados en fase LOAD en la tabla weather_hourl
├── .env.example                 # Template de variables de entorno
├── .gitignore
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

##  Instalación y Uso

### Prerrequisitos

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado y corriendo
- Git

### Paso 1 — Clonar el repositorio

```bash
git clone https://github.com/PoliticalDog/weather-etl-pipeline
cd weather-etl-pipeline
```

### Paso 2 — Configurar variables de entorno

```bash
cp .env.example .env
```

Abre el archivo `.env` y completa los valores. Para generar la Fernet key requerida por Airflow:

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

Pega el resultado en `AIRFLOW__CORE__FERNET_KEY` dentro de tu `.env`.

### Paso 3 — Levantar PostgreSQL

```bash
docker compose up -d postgres
```

Espera a que el contenedor esté `healthy`:

```bash
docker compose ps
```

### Paso 4 — Inicializar Airflow

```bash
docker compose run --rm airflow-init
```

Espera a que aparezca el mensaje `Admin user admin created`.

### Paso 5 — Levantar todos los servicios

```bash
docker compose up -d
```

### Paso 6 — Acceder a los servicios

| Servicio | URL | Credenciales |
|---|---|---|
| Airflow UI | http://localhost:8080 | admin / admin |
| pgAdmin | http://localhost:5050 | admin@admin.com / admin |

### Paso 7 — Ejecutar el pipeline

1. Entra a http://localhost:8080
2. Activa el DAG `weather_etl_pipeline` con el toggle
3. Click en ▶ **Trigger DAG** para ejecutarlo manualmente
4. Verifica que las 3 tareas (extract → transform → load) terminen en verde

### Paso 8 — Verificar los datos

Desde pgAdmin conecta a PostgreSQL con:
- Host: `postgres`
- Port: `5432`
- Database: `airflow`
- Username: `airflow`
- Password: `airflow`

O desde terminal:

```bash
docker compose exec postgres psql -U airflow -d airflow -c "SELECT * FROM weather_hourly LIMIT 10;"
```

---

##  Variables de Entorno

| Variable | Descripción |
|---|---|
| `POSTGRES_USER` | Usuario de PostgreSQL |
| `POSTGRES_PASSWORD` | Contraseña de PostgreSQL |
| `POSTGRES_DB` | Nombre de la base de datos |
| `POSTGRES_HOST` | Host de PostgreSQL (usar `postgres` en Docker) |
| `POSTGRES_PORT` | Puerto de PostgreSQL |
| `AIRFLOW__CORE__FERNET_KEY` | Key de cifrado de Airflow (generar con comando arriba) |
| `AIRFLOW__WEBSERVER__SECRET_KEY` | Secret key del webserver de Airflow |
| `AIRFLOW__DATABASE__SQL_ALCHEMY_CONN` | Cadena de conexión de Airflow a PostgreSQL |
| `WEATHER_CITY` | Nombre de la ciudad a monitorear |
| `WEATHER_LAT` | Latitud de la ciudad |
| `WEATHER_LON` | Longitud de la ciudad |

---

##  Autor

**PoliticalDog** — [github.com/PoliticalDog](https://github.com/PoliticalDog)

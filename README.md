## 🚀 Instalación

1. Clona el repo
2. Copia el archivo de entorno:
   cp .env.example .env

3. Genera tu Fernet key y pégala en .env:
   python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"

4. Levanta el entorno:
   docker compose up -d

# Probar el consumo de la api
python -c "from etl.extract import extract_weather; print(extract_weather(19.4, -99.1))"


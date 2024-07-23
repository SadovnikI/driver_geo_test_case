# README

## Project Overview

This project involves creating a system to generate random coordinates for drivers within the city of Lviv, send these coordinates to an HTTP endpoint, and process the data using a FastAPI/Flask service. The data is logged into a PostgreSQL database, with abnormal data being flagged and logged separately. The entire setup can be quickly deployed using Docker and Docker Compose.

## Project Structure

1. **Random Coordinates Script**:
   - Generates random coordinates (latitude, longitude), speed, and altitude for drivers within Lviv.
   - Sends data to the service endpoint every X seconds.
   - Configured using a `settings.json` file.

2. **FastAPI/Flask Service**:
   - Receives data via the `/api/v1/driver-geo` endpoint.
   - Logs abnormal data based on speed (>X km/h), altitude (<0 or >X meters), and realistic distance checks.
   - Stores all received data in a PostgreSQL database, marking each entry as correct or abnormal.
   - Provides Swagger documentation for easy interaction with the API.

3. **Configuration Management**:
   - Uses a `settings.json` file for storing parameters like database connection details and threshold values.

4. **Docker**:
   - Docker Compose file for easy setup and deployment of the service, script, and PostgreSQL database.

## Setup Instructions

### Prerequisites

- Docker
- Docker Compose
- Python 3.10 or higher

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/SadovnikI/driver_geo_test_case.git
   cd driver-geo-service
   ```

2. **Build and Run with Docker Compose**:
   ```bash
   docker-compose up --build
   ```

### Configuration

1. **Settings File**:
   - Modify the `settings.json` file to adjust parameters such as database connection details and threshold values (look for `settings.json.example` for quick start).
   ```json
   {
    "driver_service": {
        "endpoint_url": "http://driver_geo_web:8000/api/v1/driver-geo/",
        "send_interval_seconds": 10
    },
    "drivers": {
        "number_of_drivers": 5
    },
    "location": {
        "city": "Lviv, Ukraine",
        "latitude_range": [49.795, 49.905],
        "longitude_range": [23.903, 24.043]
    },
    "data_limits": {
        "max_speed_kmh": 13,
        "min_altitude_m": 0,
        "max_altitude_m": 400
    },
    "database": {
        "host": "localhost",
        "port": 5432,
        "username": "root",
        "password": "root",
        "database_name": "test_database",
        "url": "postgresql+asyncpg://postgres:postgres@postgres_db:5432/test_database"
    },
    "elevation": {
        "lookup_url": "https://api.open-elevation.com/api/v1/lookup?locations={},{}"
    }
   }
   ```

2. **Alembic Configuration**:
   - Modify the `alembic.ini` file to set the `sqlalchemy.url` parameter for database connection. For a quick start, use:
   ```ini
   sqlalchemy.url = postgresql+psycopg2://root:root@localhost:5432/test_database
   ```


### Running the Project

1. **Start the Services**:
   ```bash
   docker-compose up
   ```

2. **Access the API**:
   - The API will be available at `http://localhost:8000/api/v1/driver-geo`.

3. **Swagger Documentation**:
   - For FastAPI, Swagger documentation is automatically available.
   - Access it at `http://localhost:8000/docs` for interactive API exploration.
   - The Swagger UI provides a user-friendly interface to interact with your FastAPI endpoints, view request/response schemas, and test the API directly.

### Additional Features

1. **Health Check Endpoint**:
   - To check the availability of the database, use the `/health` endpoint.
   
2. **Metrics Endpoint**:
   - Access service metrics at the `/metrics` endpoint.

### Handling Database Unavailability

- The service will attempt to reconnect to the PostgreSQL database if it becomes unavailable. Accumulated data will be written to the database once the connection is reestablished.


### Optional Enhancements

- [x] **Include Swagger documentation for the FastAPI endpoints**.
- [x] **Implement the ability to apply new settings without restarting the service when the settings file is updated**.
- [x] **Add a health-check endpoint to verify database availability**.
- [x] **Add a metrics endpoint that provides various metrics including service runtime, number of received coordinates, unique drivers, speed violations, altitude anomalies, and total records**.


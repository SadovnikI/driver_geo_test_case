import json
from typing import List
from pydantic_settings import BaseSettings
import os


class DriverServiceSettings(BaseSettings):
    endpoint_url: str
    send_interval_seconds: int


class DriverSettings(BaseSettings):
    number_of_drivers: int


class LocationSettings(BaseSettings):
    city: str
    latitude_range: List[float]
    longitude_range: List[float]


class DataLimitsSettings(BaseSettings):
    max_speed_kmh: int
    min_altitude_m: int
    max_altitude_m: int


class DatabaseSettings(BaseSettings):
    host: str
    port: int
    username: str
    password: str
    database_name: str
    url: str


class ElevationSettings(BaseSettings):
    lookup_url: str


class Settings(BaseSettings):
    driver_service: DriverServiceSettings
    drivers: DriverSettings
    location: LocationSettings
    data_limits: DataLimitsSettings
    database: DatabaseSettings
    elevation: ElevationSettings


base_dir = os.path.dirname(os.path.abspath(__file__))
settings_path = os.path.join(base_dir, 'settings.json')


def load_settings() -> Settings:
    with open(settings_path, 'r', encoding='utf-8') as f:
        config_data = json.load(f)
    return Settings(**config_data)


settings = load_settings()

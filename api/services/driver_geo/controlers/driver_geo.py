import time
from typing import Dict, Any

from tenacity import RetryError

from api.database.session import check_db_connection
from api.services.driver_geo.models.driver import DriverDataRepository
from api.services.driver_geo.schemas.base import BasicResponse, ApiMetrics
from api.services.driver_geo.schemas.driver_geo import DriverDataRequestSchema, DriverDataResponseSchema
from api.services.driver_geo.utils.database import retry_to_save_to_db
from api.services.driver_geo.utils.map import get_shortest_path_length
from config import settings
from constants.core.buffered_data import buffered_data
from constants.core.logs import logger
from constants.core.metrics import metrics
from fastapi import status

from constants.map.core import city_G


async def update_driver_geo(driver_data: DriverDataRequestSchema,
                            repository: DriverDataRepository) -> DriverDataResponseSchema:
    """
    Updates the driver's geographic data, validates it, and saves it to the database.

    Args:
        driver_data (DriverDataRequestSchema): The incoming driver data to be processed.
        repository (DriverDataRepository): Repository instance for database operations.

    Returns:
        DriverDataResponseSchema: The response schema containing the processed data.
    """
    driver_id = driver_data.driver_id

    metrics["total_coordinates"] += 1
    metrics["unique_drivers"].add(driver_id)

    previous_data = buffered_data[driver_id][-1] if len(buffered_data[driver_id]) > 0 else None
    is_correct = validate_driver_data(driver_data, previous_data)

    if not is_correct:
        logger.warning(f"Anomalous data detected: {driver_data.model_dump()}")

    current_data = driver_data.model_dump()
    current_data['is_correct'] = is_correct
    buffered_data[driver_id].append(current_data)
    await save_buffered_data(driver_id, repository)

    return DriverDataResponseSchema(**current_data)


def validate_driver_data(driver_data: DriverDataRequestSchema, previous_data: Dict[str, Any]) -> bool:
    """
    Validates the driver's geographic data against predefined limits and previous data.

    Args:
        driver_data (DriverDataRequestSchema): The incoming driver data to be validated.
        previous_data (Dict[str, Any]): The previous data for comparison, if available.

    Returns:
        bool: True if the data is correct, False otherwise.
    """
    is_correct = True

    if driver_data.speed > settings.data_limits.max_speed_kmh:
        is_correct = False
        metrics["speed_violations"] += 1
        logger.info(f"Speed violation detected: {driver_data.speed} km/h")

    if driver_data.altitude < settings.data_limits.min_altitude_m or driver_data.altitude > settings.data_limits.max_altitude_m:
        is_correct = False
        metrics["altitude_violations"] += 1
        logger.info(f"Altitude violation detected: {driver_data.altitude} m")

    if previous_data:
        distance = get_shortest_path_length(
            driver_data.longitude,
            driver_data.latitude,
            previous_data["longitude"],
            previous_data["latitude"],
            city_G
        )

        max_possible_distance = (settings.data_limits.max_speed_kmh * 1000 / 3600) * settings.driver_service.send_interval_seconds
        if distance > max_possible_distance:
            is_correct = False
            metrics["distance_violations"] += 1
            logger.info(f"Distance violation detected: {distance} meters")

    return is_correct


async def save_buffered_data(driver_id: str, repository: DriverDataRepository):
    """
    Saves buffered driver data to the database and handles potential retries.

    Args:
        driver_id (str): The ID of the driver whose data is being saved.
        repository (DriverDataRepository): Repository instance for database operations.
    """
    for item in buffered_data[driver_id][:-1]:
        try:
            await retry_to_save_to_db(repository, item)
            buffered_data[driver_id].remove(item)
            logger.info(f"Successfully saved data to DB: {item}")
        except RetryError as e:
            logger.error(f"Failed to write to DB: {item} \n {e}")


async def health_check() -> BasicResponse:
    """
    Performs a health check to verify the database connection.

    Returns:
        BasicResponse: Response indicating the health status of the service.
    """
    if await check_db_connection():
        logger.info("Health check passed.")
        return BasicResponse(status=status.HTTP_200_OK, message="healthy")
    else:
        logger.error("Health check failed.")
        return BasicResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR, message="unhealthy")


def get_metrics() -> ApiMetrics:
    """
    Retrieves the current metrics of the service.

    Returns:
        ApiMetrics: The current metrics summary of the service.
    """
    metrics_summary = {
        "uptime": time.time() - metrics["start_time"],
        "total_coordinates": metrics["total_coordinates"],
        "unique_drivers": len(metrics["unique_drivers"]),
        "speed_violations": metrics["speed_violations"],
        "altitude_violations": metrics["altitude_violations"],
        "db_records": metrics["db_records"]
    }
    logger.info(f"Metrics summary: {metrics_summary}")
    return ApiMetrics(**metrics_summary)

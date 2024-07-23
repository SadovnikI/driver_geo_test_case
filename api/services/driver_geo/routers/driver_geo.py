from fastapi import APIRouter, Body
from api.services.driver_geo.controlers.driver_geo import update_driver_geo, health_check, get_metrics
from api.services.driver_geo.models.driver import DriverDataRepository
from api.services.driver_geo.schemas.base import ApiMetrics, BasicResponse
from api.services.driver_geo.schemas.driver_geo import DriverDataRequestSchema, DriverDataResponseSchema
from config import settings, load_settings, Settings
from constants.core.logs import logger

router = APIRouter()


@router.post("/driver-geo/",
             summary="Update Driver Geographic Data",
             description="Endpoint to update the geographic data of a driver based on provided information.",
             response_description="The response will include the processed driver data.",
             response_model=DriverDataResponseSchema)
async def update_driver_geo_handler(
        repository: DriverDataRepository,
        driver_data: DriverDataRequestSchema = Body(...)) -> DriverDataResponseSchema:
    """
    Handles the update of driver geographic data.

    Args:
        repository (DriverDataRepository): Repository instance for database operations.
        driver_data (DriverDataRequestSchema): The incoming driver data to be processed.

    Returns:
        DriverDataResponseSchema: The response schema containing the processed data.
    """
    logger.info(f"Received driver data for update: {driver_data}")
    response = await update_driver_geo(driver_data, repository)
    logger.info(f"Driver data update response: {response}")
    return response


@router.get("/health-check",
            summary="Check Service Health",
            description="Endpoint to check the health status of the service.",
            response_description="The response will indicate if the service is healthy.",
            response_model=BasicResponse)
async def health_check_handler() -> BasicResponse:
    """
    Handles the health check of the service.

    Returns:
        BasicResponse: Response indicating the health status of the service.
    """
    response = await health_check()
    logger.info(f"Health check response: {response}")
    return response


@router.get("/metrics",
            summary="Get Service Metrics",
            description="Endpoint to retrieve current service metrics.",
            response_description="The response will include current service metrics.",
            response_model=ApiMetrics)
def get_metrics_handler() -> ApiMetrics:
    """
    Retrieves and returns current service metrics.

    Returns:
        ApiMetrics: The current metrics summary of the service.
    """
    metrics_summary = get_metrics()
    logger.info(f"Metrics summary: {metrics_summary}")
    return metrics_summary


@router.get("/settings",
            summary="Retrieve Current Settings",
            description="Endpoint to retrieve the current settings of the service.",
            response_description="The response will include the current settings.",
            response_model=Settings)
def get_settings() -> Settings:
    """
    Retrieves and returns the current settings.

    Returns:
        Settings: The current settings of the service.
    """
    return settings


@router.post("/settings/reload",
             summary="Reload Settings",
             description="Endpoint to reload the service settings.",
             response_description="The response will include the reloaded settings.",
             response_model=Settings)
def reload_settings() -> Settings:
    """
    Reloads and returns the updated settings.

    Returns:
        Settings: The reloaded settings of the service.
    """
    global settings
    settings = load_settings()
    return settings

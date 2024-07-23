from fastapi import FastAPI
from api.services.driver_geo.routers import router as DriverGeoRouter

app = FastAPI(
    title="Driver Geo Test",
    docs_url="/docs",
    openapi_url="/openapi.json",
)

app.include_router(DriverGeoRouter, tags=['Driver geo'], prefix='/api/v1')


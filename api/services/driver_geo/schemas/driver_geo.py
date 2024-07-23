from uuid import UUID

from pydantic import BaseModel, Field, constr, confloat


class DriverDataRequestSchema(BaseModel):
    """
    Schema for incoming driver data requests.
    """
    driver_id: UUID = Field(..., description="Unique identifier for the driver")
    latitude: confloat(gt=-90, lt=90) = Field(..., description="Latitude coordinate of the driver's location")
    longitude: confloat(gt=-180, lt=180) = Field(..., description="Longitude coordinate of the driver's location")
    speed: confloat(ge=0) = Field(..., description="Current speed of the driver in km/h")
    altitude: confloat(ge=-430, le=8850) = Field(..., description="Current altitude of the driver in meters")

    class Config:
        json_schema_extra = {
            "example": {
                "driver_id": "1c6921bc-deae-4a56-8123-7056c6b62901",
                "latitude": 37.7749,
                "longitude": -122.4194,
                "speed": 60.0,
                "altitude": 15.0
            }
        }

    def model_dump(self, *args, **kwargs):
        data = super().model_dump(*args, **kwargs)
        if isinstance(data.get('driver_id'), UUID):
            data['driver_id'] = str(data['driver_id'])
        return data


class DriverDataResponseSchema(DriverDataRequestSchema):
    """
    Schema for the response of driver data requests, extending DriverDataRequestSchema.
    """
    is_correct: bool = Field(..., description="Indicates if anomalies detected")

    class Config:
        json_schema_extra = {
            "example": {
                "driver_id": "12345",
                "latitude": 37.7749,
                "longitude": -122.4194,
                "speed": 60.0,
                "altitude": 15.0,
                "is_correct": True
            }
        }

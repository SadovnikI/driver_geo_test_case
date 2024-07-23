import datetime

import status as status
from pydantic import BaseModel, Field
from fastapi import status


class BasicResponse(BaseModel):
    """
    Represents a basic response with a message and status code.
    """

    message: str = Field(..., description="Message describing the response.")
    status: int = Field(
        status.HTTP_200_OK,
        description="HTTP status code of the response. Defaults to 200.",
        ge=100, le=599  # Valid HTTP status code range
    )

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Successful",
                "status": status.HTTP_200_OK
            }
        }


class ApiMetrics(BaseModel):
    uptime: datetime.timedelta = Field(..., description="Time duration since the service started")
    total_coordinates: int = Field(..., description="Total number of coordinates processed")
    unique_drivers: int = Field(..., description="Number of unique drivers recorded")
    speed_violations: int = Field(..., description="Number of speed violations detected")
    altitude_violations: int = Field(..., description="Number of altitude violations detected")
    db_records: int = Field(..., description="Number of records saved to the database")

    class Config:
        json_schema_extra = {
            "example": {
                "uptime": "1 day, 1:33:21",  # Example format of timedelta
                "total_coordinates": 44,
                "unique_drivers": 13,
                "speed_violations": 32,
                "altitude_violations": 11,
                "db_records": 14
            }
        }

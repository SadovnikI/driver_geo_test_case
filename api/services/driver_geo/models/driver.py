from datetime import datetime
import uuid
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Float, Boolean, DateTime, Index
from sqlalchemy.dialects.postgresql import UUID
from api.database.models import Base
from api.database.repository import DatabaseRepository
from api.services.driver_geo.controlers.dependencies import get_repository


class DriverData(Base):
    """
    SQLAlchemy model for storing driver data.
    """

    __tablename__ = "driver_data"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    driver_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), index=True)
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    altitude: Mapped[float] = mapped_column(Float)
    speed: Mapped[float] = mapped_column(Float)
    is_correct: Mapped[bool] = mapped_column(Boolean)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index('idx_driver_id', 'driver_id'),
    )


DriverDataRepository = Annotated[
    DatabaseRepository[DriverData],
    Depends(get_repository(DriverData)),
]

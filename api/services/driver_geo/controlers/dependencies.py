from collections.abc import Callable

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.database.models import Base
from api.database.repository import DatabaseRepository
from api.database.session import get_db_session


def get_repository(
    model: type[Base],
) -> Callable[[AsyncSession], DatabaseRepository]:
    def func(session: AsyncSession = Depends(get_db_session)):
        return DatabaseRepository(model, session)
    return func

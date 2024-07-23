from collections.abc import AsyncGenerator
from sqlalchemy import text
from sqlalchemy import exc
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.exc import SQLAlchemyError
from config import settings


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    engine = create_async_engine(settings.database.url)
    factory = async_sessionmaker(engine)
    async with factory() as session:
        try:
            yield session
            await session.commit()
        except exc.SQLAlchemyError:
            await session.rollback()
            raise


async def check_db_connection() -> bool:
    engine = create_async_engine(settings.database.url)
    async with engine.connect() as conn:
        try:
            await conn.execute(text("SELECT 1"))
            return True
        except SQLAlchemyError:
            return False

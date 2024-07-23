from typing import Dict

from tenacity import retry, stop_after_attempt, wait_fixed

from api.database.repository import DatabaseRepository
from constants.core.logs import logger
from constants.core.metrics import metrics


@retry(stop=stop_after_attempt(5), wait=wait_fixed(1))
async def retry_to_save_to_db(repository: DatabaseRepository, data: Dict) -> None:
    """
    Attempts to save data to the database with retries on failure.

    Args:
        repository (DatabaseRepository): The repository instance to interact with the database.
        data (Dict): The data to be saved in the database.

    Raises:
        Exception: Re-raises the exception to allow retry logic to handle it.
    """
    try:
        await repository.create(data)
        metrics["db_records"] += 1
        logger.info(f"Successfully saved data to DB: {data}")
        logger.info(f"Updated database record count: {metrics['db_records']}")
    except Exception as e:
        logger.error(f"Error saving data to DB: {data} \nException: {e}")

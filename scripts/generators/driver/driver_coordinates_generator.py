import uuid
from threading import Timer

from config import settings
from constants.core.logs import logger
from constants.map.core import city_edges
from scripts.generators.utils.map import generate_random_points_on_roads, generate_driver_data, send_driver_data


def driver_coordinates_generator(num_drivers: int, interval: int, endpoint: str) -> None:
    """
    Generates and sends driver data at regular intervals.

    Args:
        num_drivers (int): The number of drivers to generate data for.
        interval (int): The time interval (in seconds) between each data generation and sending.
        endpoint (str): The URL endpoint to which the driver data will be sent.
    """
    driver_ids = [uuid.uuid4() for _ in range(num_drivers)]

    def update_and_send_data() -> None:
        try:
            random_points = generate_random_points_on_roads(city_edges, num_drivers)
            drivers_data = [generate_driver_data(driver_id, point) for driver_id, point in
                            zip(driver_ids, random_points)]
            logger.info(f"Generated driver data: {drivers_data}")

            for driver_data in drivers_data:
                try:
                    send_driver_data(driver_data, endpoint)
                except Exception as e:
                    logger.error(f"Failed to send driver data: {driver_data} \nException: {e}")

        except Exception as e:
            logger.error(f"Error generating driver data: {e}")
        finally:
            Timer(interval, update_and_send_data).start()

    update_and_send_data()


if __name__ == "__main__":
    # Retrieve settings from configuration
    NUM_DRIVERS = settings.drivers.number_of_drivers
    INTERVAL = settings.driver_service.send_interval_seconds
    ENDPOINT = settings.driver_service.endpoint_url

    # Start the driver coordinates generator
    driver_coordinates_generator(NUM_DRIVERS, INTERVAL, ENDPOINT)

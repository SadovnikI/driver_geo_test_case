from typing import Dict, Union, Optional, List
from uuid import UUID

import requests
import random
from geopandas import GeoDataFrame
from shapely import Point
from shapely.geometry import LineString
from api.services.driver_geo.schemas.driver_geo import DriverDataRequestSchema
from config import settings
from constants.core.logs import logger


def random_point_on_line(line: LineString) -> Point:
    """
    Generates a random point on a given LineString.

    Args:
        line (LineString): The LineString on which to generate the random point.

    Returns:
        Point: The generated random point on the LineString.
    """
    distance = random.uniform(0, line.length)
    point = line.interpolate(distance)
    return point


def generate_random_points_on_roads(roads: GeoDataFrame, num_points: int) -> List[Point]:
    """
    Generates a list of random points on roads from a GeoDataFrame.

    Args:
        roads (GeoDataFrame): GeoDataFrame containing road geometries.
        num_points (int): Number of random points to generate.

    Returns:
        List[Point]: A list of generated random points.
    """
    points = []
    while len(points) < num_points:
        random_road = roads.sample()
        line = random_road.geometry.values[0]
        if isinstance(line, LineString):
            point = random_point_on_line(line)
            points.append(point)
        elif isinstance(line, (list, tuple)) and all(isinstance(part, LineString) for part in line):
            for part in line:
                point = random_point_on_line(part)
                points.append(point)
                if len(points) >= num_points:
                    break
    return points


def get_altitude(latitude: float, longitude: float) -> Optional[float]:
    """
    Retrieves the altitude for given latitude and longitude from an external API.

    Args:
        latitude (float): Latitude of the location.
        longitude (float): Longitude of the location.

    Returns:
        Optional[float]: The altitude in meters, or None if the request fails or no result is found.
    """
    url = settings.elevation.lookup_url.format(latitude, longitude)
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        results = response.json().get("results")
        if results:
            return results[0].get("elevation")
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve altitude: {e}")
    return None


def generate_driver_data(driver_id: UUID, point: Point) -> Dict[str, Union[str, float]]:
    """
    Generates driver data based on a given driver ID and geographic point.

    Args:
        driver_id (UUID): The unique identifier for the driver.
        point (Point): The geographic point for the driver's location.

    Returns:
        Dict[str, Union[str, float]]: The generated driver data as a dictionary.
    """
    altitude = get_altitude(point.y, point.x)
    driver_data = DriverDataRequestSchema(
        driver_id=driver_id,
        latitude=point.y,
        longitude=point.x,
        speed=random.uniform(0, 120),
        altitude=altitude if altitude is not None else random.uniform(200, 400)
    )
    return driver_data.model_dump()


def send_driver_data(driver_data: Dict[str, Union[str, float]], endpoint: str) -> None:
    """
    Sends driver data to a specified endpoint via HTTP POST request.

    Args:
        driver_data (Dict[str, Union[str, float]]): The driver data to be sent.
        endpoint (str): The URL endpoint to which the data will be sent.
    """
    try:
        response = requests.post(endpoint, json=driver_data)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        logger.info(f"Sent data for driver {driver_data['driver_id']}: {response.status_code}")
    except requests.RequestException as e:
        logger.error(f"Failed to send driver data: {e}")

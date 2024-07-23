import networkx as nx
import osmnx as ox

from constants.core.logs import logger
from constants.map.core import city_G


def get_shortest_path_length(
        original_longitude: float,
        original_latitude: float,
        destination_longitude: float,
        destination_latitude: float,
        city_G: nx.Graph) -> float:
    """
    Computes the shortest path length between two geographic coordinates using a graph.

    Args:
        original_longitude (float): Longitude of the starting point.
        original_latitude (float): Latitude of the starting point.
        destination_longitude (float): Longitude of the destination point.
        destination_latitude (float): Latitude of the destination point.
        city_G (nx.Graph): The graph representing the city's street network.

    Returns:
        float: The length of the shortest path between the two points in meters.

    Raises:
        ValueError: If nodes cannot be found for the given coordinates.
        NetworkXNoPath: If no path exists between the two nodes.
    """
    try:
        # Find nearest nodes in the graph
        original_node = ox.distance.nearest_nodes(city_G, original_longitude, original_latitude)
        destination_node = ox.distance.nearest_nodes(city_G, destination_longitude, destination_latitude)

        if original_node is None or destination_node is None:
            raise ValueError("One or both of the nearest nodes could not be found for the given coordinates.")

        # Uncomment to draw a path plot on map
        # distance = nx.shortest_path(city_G, original_node, destination_node, weight='length')
        # route_map = ox.plot_graph_route(city_G, distance)

        # Compute the shortest path length
        route_length = nx.shortest_path_length(city_G, original_node, destination_node, weight='length')

        logger.info(
            f"Shortest path length from ({original_latitude}, {original_longitude}) to ({destination_latitude}, {destination_longitude}): {route_length} meters")

        return route_length

    except ValueError as ve:
        logger.error(f"Value error: {ve}")
        raise
    except nx.NetworkXNoPath as np:
        logger.error(f"No path found between nodes: {np}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise

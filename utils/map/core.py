from typing import Union, Tuple

import osmnx as ox
from geopandas import GeoDataFrame
from networkx import MultiDiGraph
from pandas import DataFrame


def load_city_road_data(city_name: str) -> Tuple[MultiDiGraph, Union[Tuple[GeoDataFrame, DataFrame], GeoDataFrame, DataFrame]]:
    """
    Loads city road data from OpenStreetMap for a specified city.

    Args:
        city_name (str): The name of the city for which to load road data.

    Returns:
        Tuple[MultiDiGraph, Union[Tuple[GeoDataFrame, DataFrame], GeoDataFrame, DataFrame]]
    """
    try:
        G = ox.graph_from_place(city_name, network_type='drive')
        edges = ox.graph_to_gdfs(G, nodes=False)
        return G, edges

    except Exception as e:
        raise RuntimeError(f"Error loading road data for city '{city_name}': {e}")

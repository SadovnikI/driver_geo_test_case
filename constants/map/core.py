from config import settings
from utils.map.core import load_city_road_data

# City graph and City graph edges
city_G, city_edges = load_city_road_data(settings.location.city)

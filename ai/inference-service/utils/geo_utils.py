import numpy as np
from shapely.geometry import Point, Polygon, shape
from shapely.affinity import rotate, translate
import json
from typing import Dict, List, Tuple

def create_fire_spread_polygon(
    center_lon: float, 
    center_lat: float, 
    wind_speed: float, 
    wind_direction: float,
    hours: int
) -> Dict[str, any]:
    """
    Create a simplified fire spread prediction polygon based on wind conditions.
    This is a heuristic model that will be replaced with a proper ML model.
    """
    # Convert wind direction from meteorological to mathematical
    math_direction = (450 - wind_direction) % 360
    
    # Calculate spread distance (simplified model)
    # Base spread rate increases with wind speed
    base_spread_km = 0.2 * wind_speed * hours
    
    # Create an elliptical shape that spreads more in the wind direction
    # Major axis (downwind)
    major_axis = base_spread_km * 1.5
    
    # Minor axis (crosswind)
    minor_axis = base_spread_km * 0.7
    
    # Create ellipse points
    t = np.linspace(0, 2 * np.pi, 32)
    x = major_axis * np.cos(t)
    y = minor_axis * np.sin(t)
    
    # Rotate ellipse to align with wind direction
    angle_rad = np.radians(math_direction)
    x_rot = x * np.cos(angle_rad) - y * np.sin(angle_rad)
    y_rot = x * np.sin(angle_rad) + y * np.cos(angle_rad)
    
    # Convert to geographic coordinates (approximate)
    # 1° latitude ≈ 111 km, 1° longitude ≈ 111 km * cos(latitude)
    lat_km = 111
    lon_km = 111 * np.cos(np.radians(center_lat))
    
    # Convert km to degrees
    lon_points = center_lon + x_rot / lon_km
    lat_points = center_lat + y_rot / lat_km
    
    # Create polygon coordinates
    polygon_coords = [[lon, lat] for lon, lat in zip(lon_points, lat_points)]
    
    # Ensure polygon is closed
    if polygon_coords[0] != polygon_coords[-1]:
        polygon_coords.append(polygon_coords[0])
    
    # Create GeoJSON
    geojson = {
        "type": "Polygon",
        "coordinates": [polygon_coords]
    }
    
    return geojson

def calculate_affected_area(geojson: Dict[str, any]) -> float:
    """
    Calculate the area of a GeoJSON polygon in km².
    """
    try:
        polygon = shape(geojson)
        # Approximate area calculation (simplified)
        # For more accurate area calculation, we'd use a proper geodesic area method
        bounds = polygon.bounds
        width_km = (bounds[2] - bounds[0]) * 111 * np.cos(np.radians(bounds[1]))
        height_km = (bounds[3] - bounds[1]) * 111
        return abs(width_km * height_km)
    except:
        return 0.0

def point_in_polygon(lon: float, lat: float, geojson: Dict[str, any]) -> bool:
    """
    Check if a point is inside a GeoJSON polygon.
    """
    try:
        point = Point(lon, lat)
        polygon = shape(geojson)
        return polygon.contains(point)
    except:
        return False
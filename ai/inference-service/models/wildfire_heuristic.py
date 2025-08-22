import numpy as np
from typing import Dict, Any, Optional
from ..schemas.prediction import WildfirePredictionResult
from ..utils.geo_utils import create_fire_spread_polygon, calculate_affected_area

class WildfireHeuristicModel:
    """
    A heuristic-based wildfire spread prediction model.
    This serves as a placeholder until a proper ML model is trained and deployed.
    """
    
    def __init__(self):
        self.model_name = "wildfire_heuristic_v1"
        self.model_version = "1.0.0"
    
    def predict(self, 
                center_lon: float, 
                center_lat: float, 
                wind_speed: float, 
                wind_direction: float,
                vegetation_density: float = 0.5,
                temperature: float = 20,
                humidity: float = 50,
                hours: int = 6) -> WildfirePredictionResult:
        """
        Generate a wildfire spread prediction using heuristic rules.
        """
        # Calculate confidence based on input quality
        confidence = 0.7  # Base confidence
        
        # Adjust confidence based on vegetation density
        confidence += vegetation_density * 0.1
        
        # Adjust confidence based on temperature (higher temp = more confidence)
        if temperature > 30:
            confidence += 0.1
        elif temperature < 10:
            confidence -= 0.1
        
        # Adjust confidence based on humidity (lower humidity = more confidence)
        if humidity < 30:
            confidence += 0.1
        elif humidity > 70:
            confidence -= 0.1
        
        # Cap confidence between 0.5 and 0.9
        confidence = max(0.5, min(0.9, confidence))
        
        # Generate predicted fire perimeter
        predicted_perimeter = create_fire_spread_polygon(
            center_lon, center_lat, wind_speed, wind_direction, hours
        )
        
        # Calculate affected area
        area_affected = calculate_affected_area(predicted_perimeter)
        
        # Calculate spread distance (approx)
        spread_distance = 0.2 * wind_speed * hours * (1 + vegetation_density)
        
        # Prepare confidence factors
        confidence_factors = {
            "wind_quality": 0.8,
            "vegetation_quality": 0.6 + vegetation_density * 0.4,
            "temperature_impact": max(0, min(1, (temperature - 10) / 30)),
            "humidity_impact": max(0, min(1, (100 - humidity) / 70)),
            "model_confidence": confidence
        }
        
        return WildfirePredictionResult(
            predicted_perimeter=predicted_perimeter,
            spread_distance_km=spread_distance,
            area_affected_km2=area_affected,
            at_risk_infrastructure=None,  # Would be populated with real data
            at_risk_population=None,     # Would be populated with real data
            confidence_factors=confidence_factors
        )
    
    def predict_from_event(self, event_data: Dict[str, Any], parameters: Dict[str, Any]) -> WildfirePredictionResult:
        """
        Generate prediction from event data.
        """
        # Extract coordinates from event
        geometry = event_data.get("geometry", {})
        coordinates = None
        
        if geometry.get("type") == "Point":
            coordinates = geometry.get("coordinates", [0, 0])
        elif geometry.get("type") == "Polygon":
            # Use centroid of polygon
            coords = geometry.get("coordinates", [[[0, 0]]])
            centroid = np.mean(np.array(coords[0]), axis=0)
            coordinates = centroid.tolist()
        
        if not coordinates or len(coordinates) < 2:
            raise ValueError("Invalid event coordinates")
        
        # Extract parameters with defaults
        wind_speed = parameters.get("wind_speed", 10.0)
        wind_direction = parameters.get("wind_direction", 0.0)
        vegetation_density = parameters.get("vegetation_density", 0.5)
        temperature = parameters.get("temperature", 20.0)
        humidity = parameters.get("humidity", 50.0)
        hours = parameters.get("forecast_hours", 6)
        
        return self.predict(
            center_lon=coordinates[0],
            center_lat=coordinates[1],
            wind_speed=wind_speed,
            wind_direction=wind_direction,
            vegetation_density=vegetation_density,
            temperature=temperature,
            humidity=humidity,
            hours=hours
        )

# Create a singleton instance
wildfire_model = WildfireHeuristicModel()
import uuid
from datetime import datetime
from typing import Dict, Any, Optional, List
from ..models.wildfire_heuristic import wildfire_model
from ..services.data_fetcher import data_fetcher
from ..schemas.prediction import PredictionResponse, WildfirePredictionRequest

class PredictionService:
    """
    Main service for handling prediction requests.
    """
    
    def __init__(self):
        self.predictions = {}  # In-memory store for demo; use DB in production
    
    async def predict_wildfire(self, request: WildfirePredictionRequest, event_data: Dict[str, Any]) -> PredictionResponse:
        """
        Generate a wildfire prediction for an event.
        """
        # Generate prediction ID
        prediction_id = str(uuid.uuid4())
        
        # If parameters are not provided, try to fetch them
        parameters = request.dict(exclude={"event_id", "forecast_hours"})
        
        # If wind data is not provided, try to fetch from weather API
        if parameters.get("wind_speed") is None or parameters.get("wind_direction") is None:
            # Get event coordinates
            geometry = event_data.get("geometry", {})
            if geometry.get("type") == "Point":
                coordinates = geometry.get("coordinates", [0, 0])
                weather_data = await data_fetcher.fetch_weather_data(coordinates[1], coordinates[0])
                
                if weather_data:
                    if parameters.get("wind_speed") is None:
                        parameters["wind_speed"] = weather_data.get("wind_speed", 10.0)
                    if parameters.get("wind_direction") is None:
                        parameters["wind_direction"] = weather_data.get("wind_direction", 0.0)
                    if parameters.get("temperature") is None:
                        parameters["temperature"] = weather_data.get("temperature", 20.0)
                    if parameters.get("humidity") is None:
                        parameters["humidity"] = weather_data.get("humidity", 50.0)
        
        # If vegetation density is not provided, try to fetch it
        if parameters.get("vegetation_density") is None:
            geometry = event_data.get("geometry", {})
            if geometry.get("type") == "Point":
                coordinates = geometry.get("coordinates", [0, 0])
                vegetation_density = await data_fetcher.fetch_vegetation_data(coordinates[1], coordinates[0])
                parameters["vegetation_density"] = vegetation_density
        
        # Generate prediction
        prediction_result = wildfire_model.predict_from_event(
            event_data, 
            {**parameters, "forecast_hours": request.forecast_hours}
        )
        
        # Create response
        response = PredictionResponse(
            prediction_id=prediction_id,
            event_id=request.event_id,
            model_type="wildfire",
            forecast_hours=request.forecast_hours,
            generated_at=datetime.now(),
            confidence=prediction_result.confidence_factors.get("model_confidence", 0.7),
            result=prediction_result.dict(),
            metadata={
                "model_name": wildfire_model.model_name,
                "model_version": wildfire_model.model_version,
                "parameters_used": parameters
            }
        )
        
        # Store prediction (in memory for demo)
        self.predictions[prediction_id] = response.dict()
        
        return response
    
    async def get_prediction(self, prediction_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a stored prediction.
        """
        return self.predictions.get(prediction_id)
    
    async def get_event_predictions(self, event_id: str) -> List[Dict[str, Any]]:
        """
        Retrieve all predictions for an event.
        """
        return [pred for pred in self.predictions.values() if pred.get("event_id") == event_id]

# Create a singleton instance
prediction_service = PredictionService()
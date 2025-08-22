from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class PredictionRequest(BaseModel):
    event_id: str
    model_type: str = "wildfire"
    parameters: Optional[Dict[str, Any]] = None
    forecast_hours: int = Field(6, ge=1, le=72)

class PredictionResponse(BaseModel):
    prediction_id: str
    event_id: str
    model_type: str
    forecast_hours: int
    generated_at: datetime
    confidence: float = Field(..., ge=0, le=1)
    result: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = None

class WildfirePredictionRequest(BaseModel):
    event_id: str
    wind_speed: float = Field(..., ge=0, description="Wind speed in km/h")
    wind_direction: float = Field(..., ge=0, le=360, description="Wind direction in degrees")
    vegetation_density: Optional[float] = Field(0.5, ge=0, le=1, description="Vegetation density (0-1)")
    temperature: Optional[float] = Field(20, description="Temperature in Celsius")
    humidity: Optional[float] = Field(50, ge=0, le=100, description="Relative humidity percentage")
    forecast_hours: int = Field(6, ge=1, le=72)

class WildfirePredictionResult(BaseModel):
    predicted_perimeter: Dict[str, Any]  # GeoJSON
    spread_distance_km: float
    area_affected_km2: float
    at_risk_infrastructure: Optional[List[Dict[str, Any]]] = None
    at_risk_population: Optional[int] = None
    confidence_factors: Dict[str, float]
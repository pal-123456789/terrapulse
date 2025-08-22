from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from contextlib import asynccontextmanager
import asyncio
from typing import Dict, Any, List

from config import settings
from .schemas.prediction import PredictionRequest, PredictionResponse, WildfirePredictionRequest
from .services.prediction_service import prediction_service
from .services.data_fetcher import data_fetcher

# Mock function to fetch event data (would connect to DB in real implementation)
async def fetch_event_data(event_id: str) -> Dict[str, Any]:
    """
    Fetch event data from database.
    In a real implementation, this would query the PostGIS database.
    """
    # This is a mock implementation
    return {
        "id": event_id,
        "title": "Wildfire in Northern California",
        "category": "wildfires",
        "geometry": {
            "type": "Point",
            "coordinates": [-122.3321, 37.7749]  # San Francisco coordinates
        },
        "severity": "high"
    }

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting AI Inference Service...")
    yield
    # Shutdown
    await data_fetcher.close_session()
    print("AI Inference Service stopped.")

app = FastAPI(
    title="TerraPulse AI Inference Service",
    description="AI-powered environmental event prediction service",
    version="1.0.0",
    lifespan=lifespan
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=1000)

@app.get("/")
async def root():
    return {"message": "TerraPulse AI Inference Service"}

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "ai-inference"}

@app.post("/predict/wildfire", response_model=PredictionResponse)
async def predict_wildfire(request: WildfirePredictionRequest, background_tasks: BackgroundTasks):
    """
    Generate a wildfire spread prediction for an event.
    """
    try:
        # Fetch event data (in real implementation, from database)
        event_data = await fetch_event_data(request.event_id)
        
        if not event_data:
            raise HTTPException(status_code=404, detail="Event not found")
        
        if event_data.get("category") != "wildfires":
            raise HTTPException(status_code=400, detail="Event is not a wildfire")
        
        # Generate prediction
        prediction = await prediction_service.predict_wildfire(request, event_data)
        
        return prediction
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.get("/predictions/{prediction_id}", response_model=PredictionResponse)
async def get_prediction(prediction_id: str):
    """
    Retrieve a specific prediction by ID.
    """
    prediction = await prediction_service.get_prediction(prediction_id)
    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction not found")
    return prediction

@app.get("/events/{event_id}/predictions", response_model=List[PredictionResponse])
async def get_event_predictions(event_id: str):
    """
    Retrieve all predictions for a specific event.
    """
    predictions = await prediction_service.get_event_predictions(event_id)
    return predictions

@app.get("/models")
async def list_models():
    """
    List available prediction models.
    """
    return {
        "models": [
            {
                "id": "wildfire_heuristic",
                "name": "Wildfire Spread Prediction (Heuristic)",
                "description": "Heuristic-based wildfire spread prediction model",
                "version": "1.0.0",
                "capabilities": ["spread_prediction", "risk_assessment"],
                "parameters": {
                    "wind_speed": {"type": "float", "required": True, "description": "Wind speed in km/h"},
                    "wind_direction": {"type": "float", "required": True, "description": "Wind direction in degrees"},
                    "vegetation_density": {"type": "float", "required": False, "description": "Vegetation density (0-1)"},
                    "temperature": {"type": "float", "required": False, "description": "Temperature in Celsius"},
                    "humidity": {"type": "float", "required": False, "description": "Relative humidity percentage"},
                    "forecast_hours": {"type": "int", "required": False, "description": "Prediction timeframe in hours"}
                }
            }
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host=settings.API_HOST, 
        port=settings.API_PORT,
        reload=settings.DEBUG
    )
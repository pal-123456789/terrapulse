from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json

app = FastAPI(title="TerraPulse Inference Service")

# CORS Middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # SvelteKit dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PredictionRequest(BaseModel):
    event_id: str
    parameters: dict  # e.g., {"wind_speed": 15, "wind_direction": 270}

@app.post("/predict/wildfire")
async def predict_wildfire(request: PredictionRequest):
    """A simple heuristic-based fire spread prediction endpoint."""
    # TODO: Replace with actual ML model inference
    wind_speed = request.parameters.get("wind_speed", 0)
    # Simple heuristic: predict spread mainly downwind
    spread_distance_km = wind_speed * 0.5  # Placeholder calculation

    mock_prediction = {
        "event_id": request.event_id,
        "predicted_perimeter": {"type": "FeatureCollection", "features": []}, # Placeholder GeoJSON
        "calculation_method": "heuristic_v1",
        "confidence": 0.5,
        "spread_distance_km": spread_distance_km
    }

    return mock_prediction

@app.get("/health")
async def health():
    return {"status": "AI Service is healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
import aiohttp
import async_timeout
import json
from typing import Dict, Any, Optional
from ..config import settings

class DataFetcher:
    """
    Service to fetch additional data needed for predictions.
    """
    
    def __init__(self):
        self.session = None
    
    async def get_session(self):
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def close_session(self):
        if self.session:
            await self.session.close()
            self.session = None
    
    async def fetch_weather_data(self, lat: float, lon: float) -> Optional[Dict[str, Any]]:
        """
        Fetch current weather data from OpenWeatherMap API.
        """
        if not settings.OPENWEATHER_API_KEY:
            return None
            
        try:
            session = await self.get_session()
            url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={settings.OPENWEATHER_API_KEY}&units=metric"
            
            async with async_timeout.timeout(10):
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            "temperature": data.get("main", {}).get("temp"),
                            "humidity": data.get("main", {}).get("humidity"),
                            "wind_speed": data.get("wind", {}).get("speed", 0) * 3.6,  # Convert m/s to km/h
                            "wind_direction": data.get("wind", {}).get("deg", 0),
                            "conditions": data.get("weather", [{}])[0].get("main", "Unknown")
                        }
        except Exception as e:
            print(f"Error fetching weather data: {e}")
            return None
    
    async def fetch_vegetation_data(self, lat: float, lon: float) -> Optional[float]:
        """
        Placeholder for fetching vegetation density data.
        In a real implementation, this would use satellite data APIs.
        """
        # This is a simplified placeholder
        # Real implementation would use NDVI data from satellite APIs
        return 0.5  # Default medium vegetation density

# Create a singleton instance
data_fetcher = DataFetcher()
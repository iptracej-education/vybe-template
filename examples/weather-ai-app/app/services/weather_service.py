import httpx
from typing import Optional
from app.schemas.weather_schema import WeatherLocationSchema, WeatherDataSchema


class WeatherService:
    """Service for fetching weather data using free Open-Meteo API."""
    
    def __init__(self):
        self.geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"
        self.weather_url = "https://api.open-meteo.com/v1/forecast"
        
        # Weather condition codes from Open-Meteo
        self.weather_codes = {
            0: "clear sky",
            1: "mainly clear", 
            2: "partly cloudy",
            3: "overcast",
            45: "fog",
            48: "depositing rime fog",
            51: "light drizzle",
            53: "moderate drizzle", 
            55: "dense drizzle",
            61: "slight rain",
            63: "moderate rain",
            65: "heavy rain",
            71: "slight snowfall",
            73: "moderate snowfall",
            75: "heavy snowfall",
            80: "slight rain showers",
            81: "moderate rain showers",
            82: "violent rain showers",
            95: "thunderstorm",
            96: "thunderstorm with slight hail",
            99: "thunderstorm with heavy hail"
        }
    
    async def get_coordinates(self, location: str) -> Optional[WeatherLocationSchema]:
        """Get coordinates for a location using Open-Meteo geocoding API (completely free)."""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    self.geocoding_url,
                    params={
                        "name": location,
                        "count": 1,
                        "language": "en"
                    },
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("results"):
                        result = data["results"][0]
                        return WeatherLocationSchema(
                            city=result["name"],
                            country=result.get("country", "Unknown"),
                            lat=result["latitude"],
                            lon=result["longitude"]
                        )
                        
            except Exception as e:
                print(f"Geocoding error: {e}")
        
        # Fallback coordinates for popular cities
        fallback_coords = {
            "new york": (40.7128, -74.0060, "US"),
            "london": (51.5074, -0.1278, "UK"),
            "paris": (48.8566, 2.3522, "FR"),
            "tokyo": (35.6762, 139.6503, "JP"),
            "berlin": (52.5200, 13.4050, "DE"),
            "sydney": (-33.8688, 151.2093, "AU"),
            "moscow": (55.7558, 37.6173, "RU"),
            "beijing": (39.9042, 116.4074, "CN"),
            "mumbai": (19.0760, 72.8777, "IN"),
            "rio de janeiro": (-22.9068, -43.1729, "BR")
        }
        
        location_lower = location.lower()
        if location_lower in fallback_coords:
            lat, lon, country = fallback_coords[location_lower]
            return WeatherLocationSchema(
                city=location.title(),
                country=country,
                lat=lat,
                lon=lon
            )
        
        return None
    
    async def get_weather_data(self, location: WeatherLocationSchema) -> Optional[WeatherDataSchema]:
        """Get current weather data using Open-Meteo API (completely free)."""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    self.weather_url,
                    params={
                        "latitude": location.lat,
                        "longitude": location.lon,
                        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m"
                    },
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    current = data.get("current", {})
                    
                    # Get weather description from code
                    weather_code = current.get("weather_code", 0)
                    description = self.weather_codes.get(weather_code, "unknown conditions")
                    
                    return WeatherDataSchema(
                        location=f"{location.city}, {location.country}",
                        temperature=round(current.get("temperature_2m", 0), 1),
                        description=description,
                        humidity=current.get("relative_humidity_2m", 0),
                        wind_speed=round(current.get("wind_speed_10m", 0), 1),
                        feels_like=round(current.get("apparent_temperature", 0), 1)
                    )
                    
            except Exception as e:
                print(f"Weather API error: {e}")
        
        return None
from pydantic import BaseModel
from typing import Optional


class WeatherQuerySchema(BaseModel):
    """Schema for natural language weather queries."""
    query: str
    location: Optional[str] = None


class WeatherLocationSchema(BaseModel):
    """Schema for extracted location information."""
    city: str
    country: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None


class WeatherDataSchema(BaseModel):
    """Schema for weather data response."""
    location: str
    temperature: float
    description: str
    humidity: int
    wind_speed: float
    feels_like: float


class WeatherResponseSchema(BaseModel):
    """Schema for API response with natural language."""
    query: str
    location: WeatherLocationSchema
    weather: WeatherDataSchema
    natural_response: str
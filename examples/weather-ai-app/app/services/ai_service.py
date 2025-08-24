import os
import re
from typing import Optional
from openai import OpenAI
from app.schemas.weather_schema import WeatherDataSchema


class AIService:
    """Service for natural language processing and response generation."""
    
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.openai_api_key) if self.openai_api_key else None
    
    async def extract_location(self, query: str) -> Optional[str]:
        """Extract location from natural language query using OpenAI."""
        if not self.client:
            return self._extract_location_fallback(query)
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system", 
                        "content": "Extract the location/city name from the weather query. Return only the city name, or 'New York' if no clear location is mentioned."
                    },
                    {
                        "role": "user", 
                        "content": query
                    }
                ],
                max_tokens=50,
                temperature=0
            )
            
            location = response.choices[0].message.content.strip()
            return location if location else "New York"
            
        except Exception as e:
            print(f"OpenAI API error for location extraction: {e}")
            return self._extract_location_fallback(query)
    
    def _extract_location_fallback(self, query: str) -> Optional[str]:
        """Fallback location extraction using regex patterns."""
        patterns = [
            r"in\s+([A-Za-z\s,]+?)(?:\s|$|\?|!|,)",
            r"for\s+([A-Za-z\s,]+?)(?:\s|$|\?|!|,)", 
            r"at\s+([A-Za-z\s,]+?)(?:\s|$|\?|!|,)",
            r"([A-Za-z\s,]+?)\s+weather",
            r"weather\s+in\s+([A-Za-z\s,]+?)(?:\s|$|\?|!|,)"
        ]
        
        query_lower = query.lower()
        for pattern in patterns:
            match = re.search(pattern, query_lower)
            if match:
                location = match.group(1).strip()
                # Filter out common non-location words
                if location not in ["the", "a", "an", "today", "tomorrow", "now", "there", "it"]:
                    return location.title()
        
        return "New York"
    
    async def generate_natural_response(self, query: str, weather_data: WeatherDataSchema) -> str:
        """Generate natural language response based on query and weather data."""
        if not self.client:
            return self._generate_fallback_response(query, weather_data)
        
        try:
            weather_context = f"""
Current weather in {weather_data.location}:
- Temperature: {weather_data.temperature}°C (feels like {weather_data.feels_like}°C)
- Conditions: {weather_data.description}
- Humidity: {weather_data.humidity}%
- Wind Speed: {weather_data.wind_speed} m/s
"""
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful weather assistant. Answer the user's weather question in a conversational, natural way based on the provided weather data. Be concise but informative."
                    },
                    {
                        "role": "user",
                        "content": f"Question: {query}\n\nWeather Data: {weather_context}"
                    }
                ],
                max_tokens=150,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"OpenAI API error for response generation: {e}")
            return self._generate_fallback_response(query, weather_data)
    
    def _generate_fallback_response(self, query: str, weather_data: WeatherDataSchema) -> str:
        """Generate fallback response without OpenAI."""
        query_lower = query.lower()
        
        if "hot" in query_lower or "cold" in query_lower:
            if weather_data.temperature > 25:
                temp_desc = "quite warm"
            elif weather_data.temperature > 15:
                temp_desc = "pleasant"
            elif weather_data.temperature > 5:
                temp_desc = "cool"
            else:
                temp_desc = "cold"
            
            return f"It's currently {temp_desc} in {weather_data.location} at {weather_data.temperature}°C. The weather is {weather_data.description}."
        
        elif "rain" in query_lower or "sunny" in query_lower or "cloud" in query_lower:
            return f"The weather in {weather_data.location} is {weather_data.description}. Temperature is {weather_data.temperature}°C with {weather_data.humidity}% humidity."
        
        else:
            return f"In {weather_data.location}, it's currently {weather_data.temperature}°C and {weather_data.description}. It feels like {weather_data.feels_like}°C with {weather_data.humidity}% humidity and wind at {weather_data.wind_speed} m/s."
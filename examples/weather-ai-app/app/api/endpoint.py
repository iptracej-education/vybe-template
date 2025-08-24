from fastapi import APIRouter
from starlette.responses import JSONResponse
from http import HTTPStatus

from app.schemas.weather_schema import WeatherQuerySchema, WeatherResponseSchema
from app.services.weather_service import WeatherService
from app.services.ai_service import AIService

"""
Weather Query Endpoint Module

This module defines the FastAPI endpoint for natural language weather queries.
It implements:
1. Natural language query processing
2. Location extraction from text
3. Weather data retrieval
4. Natural language response generation

The endpoint follows async/await patterns for non-blocking operations
and provides structured responses with natural language summaries.
"""

router = APIRouter()

weather_service = WeatherService()
ai_service = AIService()


@router.post("/query")
async def handle_weather_query(data: WeatherQuerySchema) -> JSONResponse:
    """Handles natural language weather queries.

    This endpoint processes natural language queries about weather,
    extracts location information, fetches weather data, and returns
    both structured data and natural language responses.

    Args:
        data: The weather query with natural language text

    Returns:
        JSONResponse: Weather data with natural language response
    """
    # Extract location from natural language query
    location_text = data.location or await ai_service.extract_location(data.query)
    
    # Get location coordinates
    location = await weather_service.get_coordinates(location_text)
    if not location:
        return JSONResponse(
            status_code=HTTPStatus.BAD_REQUEST,
            content={"error": f"Could not find location: {location_text}"}
        )
    
    # Get weather data
    weather_data = await weather_service.get_weather_data(location)
    if not weather_data:
        return JSONResponse(
            status_code=HTTPStatus.SERVICE_UNAVAILABLE,
            content={"error": "Weather service unavailable"}
        )
    
    # Generate natural language response
    natural_response = await ai_service.generate_natural_response(data.query, weather_data)
    
    # Create response
    response = WeatherResponseSchema(
        query=data.query,
        location=location,
        weather=weather_data,
        natural_response=natural_response
    )
    
    return JSONResponse(
        status_code=HTTPStatus.OK,
        content=response.model_dump()
    )
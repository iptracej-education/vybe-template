from fastapi import APIRouter

from app.api import endpoint

"""
API Router Module

This module sets up the API router and includes all weather-related endpoints.
It uses FastAPI's APIRouter to group weather endpoints and provide a prefix.
"""

router = APIRouter()

router.include_router(endpoint.router, prefix="/weather", tags=["weather"])
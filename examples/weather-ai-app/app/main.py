from fastapi import FastAPI
from app.api.router import router as weather_router

app = FastAPI(
    title="Weather AI App",
    description="Weather information with natural language queries",
    version="1.0.0"
)

app.include_router(weather_router)
# Weather AI App

A weather application with natural language query processing built using the GenAI Launchpad template patterns.

## API Services Used

This application integrates with the following external APIs:

### 🌤️ **Open-Meteo API** (Primary Weather Service)
- **Purpose**: Real-time weather data and geocoding
- **Cost**: Completely FREE
- **Registration**: Not required
- **Rate Limits**: None for non-commercial use
- **Endpoints Used**:
  - Geocoding: `https://geocoding-api.open-meteo.com/v1/search`
  - Weather: `https://api.open-meteo.com/v1/forecast`
- **Data Retrieved**: Temperature, humidity, wind speed, weather conditions, location coordinates

### 🤖 **OpenAI API** (Optional - AI Enhancement)
- **Purpose**: Advanced natural language processing and response generation
- **Cost**: Pay-per-use (~$0.002 per query)
- **Registration**: Required for API key
- **Models Used**: GPT-3.5-turbo
- **Features**: Smart location extraction, contextual conversational responses
- **Fallback**: App works fully without this API using regex patterns and template responses

## Features

- 🤖 **Advanced Natural Language Processing** with OpenAI GPT-3.5
- 🌍 **Smart Location Extraction** from conversational queries  
- 🌤️ **Real Weather Data** via Open-Meteo API (completely free!)
- 💬 **Conversational Responses** tailored to your questions
- ⚡ **FastAPI** with async/await patterns
- 🆓 **No Registration Required** - real weather data with zero setup

## Quick Start

### 1. Install Dependencies
```bash
uv sync
```

### 2. Setup Environment 
```bash
cp .env.example .env
```

**Optional: For Advanced AI Responses**, add OpenAI key to `.env`:
```bash
# Get from https://platform.openai.com/api-keys (optional)
OPENAI_API_KEY=your_openai_key_here

# Weather API: Open-Meteo (already FREE - no setup needed!)
```

### 3. Start the Server
```bash
uv run uvicorn app.main:app --port 8001 --reload
```

### 4. Run Interactive Demo
```bash
python demo.py
```

## Demo Features

The demo showcases different types of natural language queries:

- **"What's the weather like in Paris?"** - Basic weather query
- **"Is it cold in London right now?"** - Temperature-focused question  
- **"Should I wear a jacket in New York?"** - Practical advice
- **"Is it raining in Tokyo today?"** - Condition-specific query
- **Travel planning queries** - Context-rich conversations

## API Usage

**Endpoint:** `POST /weather/query`

```bash
curl -X POST "http://localhost:8001/weather/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "Is it sunny in Barcelona today?"}'
```

**With OpenAI API Key:**
```json
{
  "query": "Should I bring an umbrella to Seattle?",
  "natural_response": "Based on the current weather in Seattle, it's partly cloudy with 15°C and 70% humidity. While it's not actively raining right now, Seattle can be unpredictable, so bringing a light rain jacket or umbrella wouldn't hurt!"
}
```

**Without OpenAI API Key (Uses Fallback Responses):**
```json
{
  "query": "What's the weather in Paris?",
  "location": {
    "city": "Paris",
    "country": "France",
    "lat": 48.8566,
    "lon": 2.3522
  },
  "weather": {
    "location": "Paris, France",
    "temperature": 18.3,
    "description": "partly cloudy"
  },
  "natural_response": "The weather in Paris, France is partly cloudy. Temperature is 18.3°C with 72% humidity."
}
```

## API Documentation

Visit http://localhost:8001/docs for interactive API documentation.

### Weather Query Endpoint

**POST** `/weather/query`

```json
{
  "query": "What is the weather like in Paris?",
  "location": "Paris" // optional, will extract from query if not provided
}
```

**Response:**
```json
{
  "query": "What is the weather like in Paris?",
  "location": {
    "city": "Paris",
    "country": "France",
    "lat": 48.8566,
    "lon": 2.3522
  },
  "weather": {
    "location": "Paris, France",
    "temperature": 18.3,
    "description": "partly cloudy",
    "humidity": 72,
    "wind_speed": 2.1,
    "feels_like": 17.9
  },
  "natural_response": "In Paris, France, it's currently 18.3°C and partly cloudy. It feels like 17.9°C with 72% humidity and wind at 2.1 m/s."
}
```

## Service Architecture

### API Integration Services

**`WeatherService` (`app/services/weather_service.py`)**:
- Handles Open-Meteo API integration
- Geocoding for location lookup
- Weather data retrieval with error handling
- Fallback coordinates for popular cities
- Weather condition code translation

**`AIService` (`app/services/ai_service.py`)**:
- OpenAI GPT-3.5 integration (optional)
- Location extraction from natural language
- Contextual response generation
- Intelligent fallback using regex patterns
- Template-based responses when API unavailable

### Template Patterns Used

Following GenAI Launchpad patterns:
- FastAPI application structure
- Async/await patterns throughout all API calls
- Service layer architecture for external API integration
- Dependency injection ready
- Pydantic schemas for request/response validation
- Modular service architecture with clean separation
- Error handling and fallback patterns
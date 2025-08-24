# Weather AI App - Demo Instructions

## 🚀 Quick Demo (REAL Weather Data - No API Keys Needed!)

The app gets REAL weather data completely FREE using Open-Meteo API!

### 1. Start the Server
```bash
cd weather-ai-app
uv sync
uv run uvicorn app.main:app --port 8001 --reload
```

### 2. Test Basic Functionality
```bash
# Simple query
curl -X POST "http://localhost:8001/weather/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the weather like in Paris?"}'

# Conversational query  
curl -X POST "http://localhost:8001/weather/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "Should I wear a jacket in Seattle?"}'
```

### 3. Run Interactive Demo
```bash
python demo.py
```

## 🔑 Full Demo with OpenAI API Key

### 1. Get OpenAI API Key
- Visit https://platform.openai.com/api-keys
- Create a new API key
- You'll need ~$1-2 credit for extensive testing

### 2. Setup Environment
```bash
cp .env.example .env
# Edit .env and add:
OPENAI_API_KEY=your_actual_api_key_here
```

### 3. Test Advanced AI Features
```bash
# Complex conversational query
curl -X POST "http://localhost:8001/weather/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "I am planning a picnic in Central Park tomorrow. What should I expect weather-wise?"}'
```

## 🌟 Demo Query Examples

**Basic Queries:**
- "What's the weather in London?"
- "Is it cold in New York?"

**Conversational Queries:** 
- "Should I bring an umbrella to Seattle?"
- "Is it good beach weather in Miami?"
- "What should I wear in Chicago today?"

**Travel Planning:**
- "I'm visiting Tokyo tomorrow, what's the weather forecast?"
- "Planning a hike in Denver, is it suitable weather?"

**Weather Conditions:**
- "Is it raining in Portland right now?"
- "How windy is it in San Francisco?"

## 🔧 Features Demonstrated

### Without Any Setup:
- ✅ REAL weather data from Open-Meteo API  
- ✅ Smart location extraction using regex patterns
- ✅ Accurate current weather conditions
- ✅ FastAPI structure with async/await
- ✅ Full API documentation

### With OpenAI API Key:
- 🤖 Advanced location extraction using GPT-3.5
- 💬 Contextual, conversational responses
- 🎯 Query-specific advice and recommendations
- 📝 Natural language understanding

## 📱 API Documentation

Visit http://localhost:8001/docs for interactive Swagger documentation.

## 🏗️ Template Pattern Inheritance

This app demonstrates 95% template pattern inheritance from GenAI Launchpad:
- FastAPI app structure
- Async/await patterns throughout
- Service layer architecture with external API integration
- Pydantic schemas for validation
- Router/endpoint separation
- Type-safe code patterns
- External service integration patterns (Open-Meteo, OpenAI)
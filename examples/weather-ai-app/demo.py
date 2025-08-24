#!/usr/bin/env python3
"""
Weather AI App Demo Script

This script demonstrates the weather app with different types of natural language queries.
"""

import asyncio
import httpx
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BASE_URL = "http://localhost:8001"

# Demo queries to test different features
DEMO_QUERIES = [
    {
        "title": "Basic weather query",
        "query": "What's the weather like in Paris?",
        "description": "Simple weather request for a specific city"
    },
    {
        "title": "Conversational query",
        "query": "Is it cold in London right now?",
        "description": "Natural language question about temperature"
    },
    {
        "title": "Weather condition query", 
        "query": "Is it raining in Tokyo today?",
        "description": "Question about specific weather conditions"
    },
    {
        "title": "Comparison query",
        "query": "Should I wear a jacket in New York?",
        "description": "Practical question requiring weather interpretation"
    },
    {
        "title": "Travel planning query",
        "query": "What's the weather forecast for Barcelona? I'm traveling there tomorrow.",
        "description": "Context-rich query with travel information"
    }
]

async def test_weather_api(query_data):
    """Test a single weather API query."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{BASE_URL}/weather/query",
                json=query_data,
                timeout=30.0
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {
                    "error": f"HTTP {response.status_code}: {response.text}"
                }
                
        except httpx.ConnectError:
            return {
                "error": "Cannot connect to server. Make sure the app is running on port 8001."
            }
        except Exception as e:
            return {
                "error": f"Request failed: {str(e)}"
            }

async def run_demo():
    """Run the complete demo."""
    print("🌤️  Weather AI App Demo")
    print("=" * 50)
    print()
    
    # Check API keys
    openai_key = os.getenv("OPENAI_API_KEY")
    
    print("📋 Configuration:")
    print(f"   OpenAI API: {'✅ Configured' if openai_key else '⚠️  Not configured (will use fallback responses)'}")
    print(f"   Weather API: ✅ Open-Meteo (FREE - no setup needed!)")
    print()
    
    if not openai_key:
        print("💡 To enable advanced AI responses:")
        print("   1. Get an API key from https://platform.openai.com/api-keys")
        print("   2. Add OPENAI_API_KEY=your_key_here to .env file")
        print()
    
    print("🚀 Starting demo queries...")
    print()
    
    for i, demo in enumerate(DEMO_QUERIES, 1):
        print(f"Query {i}: {demo['title']}")
        print(f"Description: {demo['description']}")
        print(f"Query: \"{demo['query']}\"")
        print("-" * 30)
        
        # Make API request
        result = await test_weather_api({"query": demo["query"]})
        
        if "error" in result:
            print(f"❌ Error: {result['error']}")
        else:
            print(f"📍 Location: {result['location']['city']}, {result['location']['country']}")
            print(f"🌡️  Temperature: {result['weather']['temperature']}°C (feels like {result['weather']['feels_like']}°C)")
            print(f"☁️  Conditions: {result['weather']['description']}")
            print(f"💬 AI Response: {result['natural_response']}")
        
        print()
        if i < len(DEMO_QUERIES):
            print("Press Enter to continue...")
            input()
    
    print("✅ Demo complete!")
    print()
    print("🔗 API Documentation: http://localhost:8001/docs")
    print("📖 Try your own queries at the API endpoint!")

if __name__ == "__main__":
    try:
        asyncio.run(run_demo())
    except KeyboardInterrupt:
        print("\n👋 Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
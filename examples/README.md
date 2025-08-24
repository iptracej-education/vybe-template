# Example Projects

This folder contains example projects generated using the Vybe Template system.

## Weather AI App

The `weather-ai-app` demonstrates:
- Template pattern inheritance from a FastAPI template
- Integration with external APIs (Open-Meteo, OpenAI)
- Service layer architecture
- Async/await patterns throughout
- Natural language processing capabilities

To try it:
```bash
cd weather-ai-app
uv sync
uv run uvicorn app.main:app --reload
```

This example shows 95% template pattern inheritance while adding domain-specific functionality.
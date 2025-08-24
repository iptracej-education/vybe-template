# Vybe Template - On-Demand Template Analysis System

**Ultra-slim CLAUDE.md generation with template pattern inheritance**

## The Problem

Current development suffers from **context overload**:
- **Massive CLAUDE.md**: 255+ lines, verbose documentation
- **Template drift**: Manual pattern copying loses fidelity
- **Real projects**: Easily reach 400-700 lines of context
- **Effectiveness loss**: Too much information dilutes AI attention

## The On-Demand Solution

**On-Demand Template Analysis**: Direct template reference for pattern inheritance

### Core Concept
1. **Reference template** (e.g., genai-launchpad) directly in CLAUDE.md
2. **Generate ultra-slim CLAUDE.md** (8 lines) with template pointer
3. **AI analyzes on-demand** - high pattern fidelity when needed
4. **Zero setup time** - instant generation, always current

### Proven Benefits
- **27% smaller context**: 11 lines → 8 lines
- **50% less AI usage**: 400+ lines → 200 lines as needed
- **Template fidelity**: Copies template patterns vs abstractions
- **Zero setup**: No extraction phase required

## Project Structure

```
vybe-template/
├── .template/                     # Your templates go here (empty by default)
├── generate-claude.py             # Main generation script
├── LICENSE                        # MIT License
└── README.md                     # This file
```

## Quick Start

### 1. Add Your Template

```bash
# Clone or copy your template into .template folder
git clone https://github.com/your-org/your-template .template/your-template
# OR
cp -r /path/to/your/template .template/my-template
```

### 2. Generate ultra-slim CLAUDE.md for your project:
```bash
# Generate from any template
./generate-claude.py /path/to/template project-name "project description [with API services]"

# Example with your template
./generate-claude.py .template/your-template my-app "app description with API services needed"

# Example with external template
./generate-claude.py ~/templates/fastapi-template weather-ai-app "weather app with Open-Meteo and OpenAI services"
```

### Result - Clean 8-line CLAUDE.md:
```markdown
# weather-ai-app
Lang: python | Framework: fastapi | Install: uv sync | Run: uv run
Template: /home/user/vybe-template/.template/genai-launchpad

## Key Files: config:pyrightconfig.json | api:kong.yml | services:__init__.py | database:pooler.sql

## Task: Create weather app with natural language queries with Open-Meteo and OpenAI services using template patterns
Analyze template on-demand → Apply async/await patterns, repository patterns → Maintain consistency
```

### Start developing:
```bash
cd your-project
cp CLAUDE.md your-project/  # Copy to your project directory
# Edit CLAUDE.md: Update project name on line 1 to match your actual project
# Example: # weather-ai-app → # my-actual-project-name
# Ultra-slim CLAUDE.md enables template pattern inheritance
# AI analyzes template on-demand for accurate pattern copying
```

## Technical Approach

On-demand template analysis uses minimal context while analyzing templates when needed. API services mentioned in the project description are integrated into the generated task specification, helping AI understand both architectural patterns and required external integrations.

### Pattern Inheritance Comparison
| **Approach** | **Context Size** | **Pattern Accuracy** | **Setup Time** |
|--------------|------------------|---------------------|----------------|
| Traditional | 255+ lines | Manual copying | Hours |
| **On-Demand** | **8 lines** | **Template copying** | **Instant** |

The AI analyzes templates directly to understand architectural patterns.

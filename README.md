# Vybe Template - Template Pattern Inheritance System

[![Project](https://img.shields.io/badge/Project-Vybe%20Template-blue)](https://github.com/yourusername/vybe-template)
[![Status](https://img.shields.io/badge/Status-Production-success)](https://github.com/yourusername/vybe-template)
[![License](https://img.shields.io/badge/License-MIT-green)](./LICENSE)
[![Python](https://img.shields.io/badge/Python-3.6+-blue)](https://www.python.org/)
[![Templates](https://img.shields.io/badge/Templates-Any%20Framework-purple)](#supported-templates)
[![Context](https://img.shields.io/badge/Context-8%20Lines-brightgreen)](#how-it-works)
[![Claude](https://img.shields.io/badge/Claude-AI%20Ready-orange)](https://claude.ai)

**🧬 Smart template pattern inheritance for AI-driven development**

> Transform any project template into an 8-line AI context file that guides architectural pattern adoption - no enforcement, just intelligent guidance.

## The Problem

Current development suffers from **context overload**:
- **Massive CLAUDE.md**: 100+ lines, verbose documentation
- **Template drift**: Manual pattern copying loses fidelity
- **Real projects**: Easily reach 400-700 lines of context
- **Effectiveness loss**: Too much information dilutes AI attention

## How It Works

**Smart Pattern Inheritance**: AI learns from templates through live analysis, not rigid enforcement

### 🎯 Pattern Inheritance Process
1. **📁 Template Reference** - Point to any project template you want to inherit from
2. **🧬 Pattern Analysis** - AI analyzes template structure, architecture, and conventions
3. **📝 Minimal Context** - Generates 8-line CLAUDE.md with template reference
4. **🤖 Guided Development** - AI naturally follows template patterns without strict enforcement
5. **🔄 Always Current** - Live template reference, patterns stay up-to-date

### 📊 Benefits

| Metric | Result | Impact |
|--------|--------|--------|
| **Context Size** | 8 lines | 📉 97% reduction vs traditional |
| **AI Token Usage** | 200 lines on-demand | 💰 Good cost savings |
| **Setup Time** | Instant | ⚡ Zero configuration |
| **Pattern Adoption** | AI-guided inheritance | 🎯 Natural pattern following |

## Project Structure

```
vybe-template/
├── .template/                     # Your templates go here (empty by default)
├── generate-claude.py             # Main generation script
├── LICENSE                        # MIT License
└── README.md                     # This file
```

## Quick Start

### 📥 Step 1: Add Your Template

```bash
# Clone or copy your template into .template folder
git clone https://github.com/your-org/your-template .template/your-template
# OR
cp -r /path/to/your/template .template/my-template
```

### ⚡ Step 2: Generate Ultra-Slim CLAUDE.md
```bash
# Generate from any template
./generate-claude.py /path/to/template project-name "project description [with API services]"

# Example with your template
./generate-claude.py .template/your-template my-app "app description with API services needed"

# Example with external template
./generate-claude.py ~/templates/fastapi-template weather-ai-app "weather app with Open-Meteo and OpenAI services"
```

### 📄 Result - Clean 8-line CLAUDE.md:
```markdown
# weather-ai-app
Lang: python | Framework: fastapi | Install: uv sync | Run: uv run
Template: /home/user/vybe-template/.template/genai-launchpad

## Key Files: config:pyrightconfig.json | api:kong.yml | services:__init__.py | database:pooler.sql

## Task: Create weather app with natural language queries with Open-Meteo and OpenAI services using template patterns
Analyze template on-demand → Apply async/await patterns, repository patterns → Maintain consistency
```

### 🎨 Step 3: Start Developing
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

### 📈 Performance Comparison

| Approach | Context Size | Pattern Accuracy | Setup Time | Maintenance |
|----------|--------------|------------------|------------|-------------|
| 🔴 **Traditional** | 100+ lines | Manual copying | Hours | Constant updates |
| 🟢 **On-Demand** | **8 lines** | Direct template | **Instant** | Zero |

## Supported Templates

### Smart Detection & Tooling
Templates with intelligent language/framework detection and proper tooling commands:

- **Python**: FastAPI, Django, Flask (with uv, poetry, pip detection)
- **JavaScript**: React, Next.js, Express (with pnpm, yarn, npm detection)

### Generic Support
Any template works with basic file scanning and generic patterns:

- **Java**: Spring Boot, Micronaut, Quarkus
- **Rust**: Actix, Rocket, Axum  
- **Go**: Gin, Echo, Fiber
- **Ruby**: Rails, Sinatra
- **.NET**: ASP.NET Core, Blazor
- **Any custom template** you create!

I would suggest to take a look at our examples and CLAUDE.md. Modify CLAUDE.md directly and put it into your project directory!  

At the same time, the detection logic in `generate-claude.py` can be easily extended to add smart support for additional languages and frameworks. Pull requests welcome!

## Contributing

We welcome contributions! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

Built for use with Claude AI and modern development workflows.

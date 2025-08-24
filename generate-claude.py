#!/usr/bin/env python3
"""
On-Demand CLAUDE.md Generator - Creates template-reference based context files

This generator creates ultra-slim CLAUDE.md files that reference templates directly
for on-demand analysis, providing template pattern inheritance.

Usage: ./generate-claude.py <template-path> <project-name> [use-case]
"""

import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from collections import Counter
import argparse


class Colors:
    """ANSI color codes for terminal output."""
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'


class TemplateStructureScanner:
    """Scans template structure to create on-demand CLAUDE.md files."""
    
    def __init__(self, template_path: str):
        self.template_path = Path(template_path)
        self.template_name = self.template_path.name
        
    def detect_language_framework(self) -> Tuple[str, str]:
        """Detect primary language and framework from template structure."""
        # Check for key files that indicate language/framework
        framework_indicators = {
            # Python frameworks
            'fastapi': ['main.py', 'app/', 'requirements.txt', 'pyproject.toml'],
            'django': ['manage.py', 'settings.py', 'apps/'],
            'flask': ['app.py', 'app/', 'requirements.txt'],
            
            # JavaScript frameworks
            'react': ['package.json', 'src/', 'public/', 'node_modules/'],
            'nextjs': ['next.config.js', 'pages/', 'components/'],
            'express': ['package.json', 'server.js', 'routes/'],
        }
        
        language_indicators = {
            'python': ['.py', 'requirements.txt', 'pyproject.toml', '__pycache__/'],
            'javascript': ['.js', '.jsx', '.ts', '.tsx', 'package.json', 'node_modules/'],
            'java': ['.java', 'pom.xml', 'build.gradle'],
            'go': ['.go', 'go.mod'],
            'rust': ['.rs', 'Cargo.toml'],
        }
        
        # Scan template files
        all_files = []
        for root, dirs, files in os.walk(self.template_path):
            # Skip hidden and common ignored directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', '.git']]
            for file in files:
                all_files.append(os.path.join(root, file))
        
        # Detect language
        language_scores = Counter()
        for lang, indicators in language_indicators.items():
            for file_path in all_files:
                for indicator in indicators:
                    if indicator in file_path:
                        language_scores[lang] += 1
        
        detected_language = language_scores.most_common(1)[0][0] if language_scores else 'unknown'
        
        # Detect framework
        framework_scores = Counter()
        for framework, indicators in framework_indicators.items():
            score = 0
            for indicator in indicators:
                if (self.template_path / indicator).exists():
                    score += 1
            if score > 0:
                framework_scores[framework] = score
        
        detected_framework = framework_scores.most_common(1)[0][0] if framework_scores else 'vanilla'
        
        return detected_language, detected_framework
    
    def find_key_files(self, language: str, framework: str) -> Dict[str, List[str]]:
        """Find key template files by category."""
        key_files = {
            'config': [],
            'api': [],
            'services': [],
            'models': [],
            'database': [],
            'async': [],
            'dependencies': [],
            'deployment': []
        }
        
        # Define search patterns by category
        search_patterns = {
            'config': ['config.py', 'settings.py', '.env.example', 'config.js', 'config.ts'],
            'api': ['endpoint.py', 'routes.py', 'api.py', 'router.py', 'routes/', 'api/', 'endpoints/'],
            'services': ['service.py', 'services/', 'worker/', 'tasks.py'],
            'models': ['models.py', 'model.py', 'schemas.py', 'models/', 'schema/'],
            'database': ['database.py', 'db.py', 'session.py', 'repository.py', 'database/', 'db/'],
            'async': ['async', 'await', 'concurrent', 'workflow'],
            'dependencies': ['dependencies.py', 'deps.py', 'providers.py'],
            'deployment': ['Dockerfile', 'docker-compose', 'deploy', '.yml', '.yaml']
        }
        
        # Scan for files
        for root, dirs, files in os.walk(self.template_path):
            # Skip hidden directories  
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            for file in files:
                if file.startswith('.'):
                    continue
                    
                rel_path = os.path.relpath(os.path.join(root, file), self.template_path)
                
                # Categorize files
                for category, patterns in search_patterns.items():
                    for pattern in patterns:
                        if pattern in rel_path.lower() or pattern in file.lower():
                            if rel_path not in key_files[category]:
                                key_files[category].append(rel_path)
        
        # Remove empty categories and limit files per category
        return {k: v[:5] for k, v in key_files.items() if v}  # Max 5 files per category
    
    def detect_tooling(self, language: str) -> Dict[str, str]:
        """Detect tooling and installation commands."""
        tooling = {}
        
        if language == 'python':
            if (self.template_path / 'uv.lock').exists():
                tooling['install'] = 'uv sync'
                tooling['run'] = 'uv run'
            elif (self.template_path / 'poetry.lock').exists():
                tooling['install'] = 'poetry install'
                tooling['run'] = 'poetry run'
            elif (self.template_path / 'pyproject.toml').exists():
                tooling['install'] = 'pip install -e .'
                tooling['run'] = 'python'
            elif (self.template_path / 'requirements.txt').exists():
                tooling['install'] = 'pip install -r requirements.txt'
                tooling['run'] = 'python'
        
        elif language == 'javascript':
            if (self.template_path / 'pnpm-lock.yaml').exists():
                tooling['install'] = 'pnpm install'
                tooling['run'] = 'pnpm run'
            elif (self.template_path / 'yarn.lock').exists():
                tooling['install'] = 'yarn install'
                tooling['run'] = 'yarn'
            elif (self.template_path / 'package.json').exists():
                tooling['install'] = 'npm install'
                tooling['run'] = 'npm run'
        
        return tooling
    
    def detect_patterns(self, key_files: Dict[str, List[str]]) -> List[str]:
        """Detect architectural patterns from key files."""
        patterns = []
        
        # Map file categories to pattern names
        if key_files.get('async'):
            patterns.append('async/await patterns')
        if key_files.get('dependencies'):
            patterns.append('dependency injection')
        if key_files.get('database'):
            patterns.append('repository patterns')
        if key_files.get('config'):
            patterns.append('configuration management')
        if key_files.get('services'):
            patterns.append('service patterns')
        if key_files.get('api'):
            patterns.append('API patterns')
        if key_files.get('deployment'):
            patterns.append('deployment patterns')
            
        return patterns
    
    def detect_template_purpose(self, language: str, framework: str, key_files: Dict[str, List[str]]) -> str:
        """Detect template purpose from structure and files."""
        # Check README or documentation for purpose hints
        readme_files = ['README.md', 'readme.md', 'README.txt', 'README.rst']
        for readme in readme_files:
            readme_path = self.template_path / readme
            if readme_path.exists():
                try:
                    with open(readme_path, 'r', encoding='utf-8') as f:
                        content = f.read().lower()
                        # Look for common project descriptions
                        if 'api' in content and ('rest' in content or 'fastapi' in content):
                            return 'API application'
                        elif 'web' in content and 'app' in content:
                            return 'web application'
                        elif 'microservice' in content:
                            return 'microservice'
                        elif 'dashboard' in content:
                            return 'dashboard application'
                        elif 'bot' in content:
                            return 'bot application'
                except:
                    pass
        
        # Fallback to framework-based detection
        if framework == 'fastapi':
            if key_files.get('api'):
                return 'API application'
            elif key_files.get('database'):
                return 'data application'
        elif framework == 'react':
            return 'frontend application'
        elif framework == 'django':
            return 'web application'
        elif framework == 'flask':
            return 'web service'
        
        # Generic fallback
        return f'{framework} application'
    
    def generate_task_description(self, project_name: str, use_case: str, template_purpose: str, patterns: List[str]) -> str:
        """Generate task description based on template analysis."""
        if use_case:
            return f"## Task: Create {use_case} using template patterns"
        else:
            return f"## Task: Create {template_purpose} using template patterns"
    
    def generate_approach_description(self, patterns: List[str]) -> str:
        """Generate approach description based on detected patterns."""
        if patterns:
            return f"Analyze template on-demand → Apply {', '.join(patterns[:2])} → Maintain consistency"
        else:
            return "Analyze template files on-demand → Copy patterns → Maintain consistency"

    def generate_ondemand_claude(self, project_name: str, use_case: str = "") -> str:
        """Generate on-demand CLAUDE.md content."""
        language, framework = self.detect_language_framework()
        tooling = self.detect_tooling(language)
        key_files = self.find_key_files(language, framework)
        patterns = self.detect_patterns(key_files)
        template_purpose = self.detect_template_purpose(language, framework, key_files)
        
        # Build header
        claude_content = f"# {project_name}\n"
        claude_content += f"Lang: {language} | Framework: {framework}"
        
        if tooling:
            install_cmd = tooling.get('install', '')
            run_cmd = tooling.get('run', '')
            if install_cmd and run_cmd:
                claude_content += f" | Install: {install_cmd} | Run: {run_cmd}\n"
            else:
                claude_content += "\n"
        else:
            claude_content += "\n"
        
        claude_content += f"Template: {self.template_path.absolute()}\n\n"
        
        # Add key template files section (compact)
        if key_files:
            claude_content += "## Key Files: "
            key_refs = []
            for category, files in key_files.items():
                if files and category in ['config', 'api', 'services', 'database', 'async']:  # Most important categories
                    key_refs.append(f"{category}:{files[0].split('/')[-1]}")  # Just filename
            claude_content += ' | '.join(key_refs[:4]) + "\n\n"  # Max 4 categories on one line
        
        # Add task section (from template analysis)
        claude_content += self.generate_task_description(project_name, use_case, template_purpose, patterns) + "\n"
        
        # Add approach (from template analysis)
        claude_content += self.generate_approach_description(patterns) + "\n"
        
        return claude_content


def print_header():
    """Print script header."""
    print(f"{Colors.BLUE}{'='*50}{Colors.END}")
    print(f"{Colors.BLUE}     ON-DEMAND CLAUDE.md GENERATOR{Colors.END}")
    print(f"{Colors.BLUE}{'='*50}{Colors.END}")
    print()


def print_usage():
    """Print usage information."""
    print("Usage: ./generate-claude.py <template-path> <project-name> [use-case]")
    print()
    print("Examples:")
    print("  ./generate-claude.py .template/genai-launchpad weather-ai-app")
    print("  ./generate-claude.py .template/genai-launchpad weather-ai-app \"weather app with Open-Meteo and OpenAI services\"")
    print("  ./generate-claude.py ~/templates/fastapi-template my-api \"REST API with auth using PostgreSQL\"")
    print()
    print("This generates an on-demand CLAUDE.md that references the template directly")
    print("for template pattern inheritance. Include API services in the use-case description.")
    print("The AI will understand both template patterns and required external integrations.")


def validate_template_path(template_path: str) -> bool:
    """Validate template path exists and is a directory."""
    if not os.path.exists(template_path):
        print(f"{Colors.RED}❌ Error: Template path '{template_path}' does not exist{Colors.END}")
        return False
    
    if not os.path.isdir(template_path):
        print(f"{Colors.RED}❌ Error: Template path '{template_path}' is not a directory{Colors.END}")
        return False
    
    return True


def main():
    """Main function."""
    # Parse arguments
    if len(sys.argv) < 3:
        print_usage()
        return 1
    
    template_path = sys.argv[1]
    project_name = sys.argv[2]
    use_case = sys.argv[3] if len(sys.argv) > 3 else ""
    
    # Print header
    print_header()
    
    # Validate template path
    if not validate_template_path(template_path):
        return 1
    
    # Display inputs
    print(f"{Colors.GREEN}📂 Template: {template_path}{Colors.END}")
    print(f"{Colors.GREEN}🎯 Project:  {project_name}{Colors.END}")
    if use_case:
        print(f"{Colors.GREEN}📝 Use Case: {use_case}{Colors.END}")
    print()
    
    print(f"{Colors.YELLOW}▶️  Scanning template structure...{Colors.END}")
    print("─" * 40)
    
    # Generate CLAUDE.md
    try:
        scanner = TemplateStructureScanner(template_path)
        claude_content = scanner.generate_ondemand_claude(project_name, use_case)
        
        # Write output
        output_file = 'CLAUDE.md'
        with open(output_file, 'w') as f:
            f.write(claude_content)
        
        print()
        print(f"{Colors.BLUE}{'='*50}{Colors.END}")
        print(f"{Colors.BLUE}        ✨ ON-DEMAND CLAUDE.md READY! ✨{Colors.END}")
        print(f"{Colors.BLUE}{'='*50}{Colors.END}")
        print()
        
        # Display the generated CLAUDE.md
        print("Generated CLAUDE.md content:")
        print("─" * 40)
        print(claude_content)
        print("─" * 40)
        print()
        
        # Success message
        print(f"{Colors.GREEN}🎉 On-demand CLAUDE.md generated successfully!{Colors.END}")
        print()
        print("Next steps:")
        print("  1. Copy CLAUDE.md to your project directory")
        print("  2. Edit CLAUDE.md: Update project name to match your actual project")
        print("  3. Start development - AI will analyze template patterns on-demand!")
        print()
        
        # Show file size
        claude_lines = len(claude_content.split('\n'))
        print(f"{Colors.BLUE}📊 CLAUDE.md: {claude_lines} lines{Colors.END}")
        
        if claude_lines <= 20:
            print(f"{Colors.GREEN}✅ Within target range (≤20 lines)!{Colors.END}")
        else:
            print(f"{Colors.YELLOW}⚠️  Slightly over target (consider optimization){Colors.END}")
        
        return 0
        
    except Exception as e:
        print(f"{Colors.RED}❌ Error generating CLAUDE.md: {e}{Colors.END}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
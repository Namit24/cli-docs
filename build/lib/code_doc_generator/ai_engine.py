import google.generativeai as genai
from typing import Dict, List
from pathlib import Path
import os
import json
import warnings


class AIDocumentationEngine:
    def __init__(self):
        self.summarizer = None
        self.gemini_model = None
        self._initialize_gemini()

    def _initialize_gemini(self):
        """Initialize Gemini AI model"""
        try:
            # Try to get API key from environment variable
            api_key = os.getenv('GEMINI_API_KEY')
            if not api_key:
                print("⚠️ GEMINI_API_KEY not found in environment variables.")
                print("Please set your Gemini API key: export GEMINI_API_KEY='your_key_here'")
                return

            genai.configure(api_key=api_key)
            self.gemini_model = genai.GenerativeModel('gemini-pro')
            print("✅ Gemini AI model loaded successfully")
        except Exception as e:
            print(f"⚠️ Could not initialize Gemini: {e}")
            self.gemini_model = None

    def _initialize_ai_models(self):
        """Fallback to transformers if Gemini is not available"""
        if self.gemini_model is None:
            try:
                from transformers import pipeline
                warnings.filterwarnings("ignore", category=UserWarning, module="transformers")
                self.summarizer = pipeline(
                    "summarization",
                    model="t5-small",
                    device=-1,
                    framework="pt"
                )
                print("✅ Fallback AI summarization model (t5-small) loaded")
            except ImportError:
                print("⚠️ Neither Gemini nor Transformers available. Using rule-based analysis.")
            except Exception as e:
                print(f"⚠️ Could not load fallback AI models: {e}")

    def generate_project_overview(self, project_analysis: Dict, project_path: Path) -> Dict:
        """Generate comprehensive project overview using Gemini AI"""
        if self.gemini_model is None:
            self._initialize_ai_models()
            return self._generate_fallback_overview(project_analysis, project_path)

        try:
            # Prepare project context for Gemini
            context = self._prepare_project_context(project_analysis, project_path)

            prompt = f"""
            Analyze this software project and provide a comprehensive overview:

            {context}

            Please provide a detailed analysis in the following JSON format:
            {{
                "project_description": "A compelling 2-3 sentence description of what this project does and its main value proposition",
                "project_type": "e.g., Web Application, CLI Tool, Machine Learning Project, etc.",
                "main_features": ["feature 1", "feature 2", "feature 3"],
                "tech_stack": ["technology 1", "technology 2"],
                "target_audience": "Who would use this project",
                "installation_steps": ["step 1", "step 2", "step 3"],
                "usage_instructions": ["how to run", "key commands", "examples"],
                "project_structure_explanation": "Brief explanation of how the project is organized"
            }}

            Make it engaging and user-friendly, similar to a good GitHub README.
            """

            response = self.gemini_model.generate_content(prompt)

            # Try to parse JSON response
            try:
                # Extract JSON from response
                response_text = response.text.strip()
                if '```json' in response_text:
                    json_start = response_text.find('```json') + 7
                    json_end = response_text.find('```', json_start)
                    json_text = response_text[json_start:json_end]
                else:
                    json_text = response_text

                overview = json.loads(json_text)
                return overview
            except json.JSONDecodeError:
                # If JSON parsing fails, create structured response from text
                return self._parse_text_response(response.text, project_analysis)

        except Exception as e:
            print(f"⚠️ Gemini API error: {e}")
            self._initialize_ai_models()
            return self._generate_fallback_overview(project_analysis, project_path)

    def _prepare_project_context(self, project_analysis: Dict, project_path: Path) -> str:
        """Prepare project context for AI analysis"""
        context_parts = []

        # Project basic info
        context_parts.append(f"Project Name: {project_analysis.get('project_name', 'Unknown')}")
        context_parts.append(f"Total Files: {project_analysis.get('total_files', 0)}")

        # Languages and technologies
        languages = set()
        technologies = set()

        for file_info in project_analysis.get('files', [])[:10]:  # Limit to first 10 files
            analysis = file_info.get('analysis', {})
            lang = analysis.get('language', '')
            if lang:
                languages.add(lang)

            # Extract technologies from imports
            imports = analysis.get('imports', [])
            for imp in imports:
                if imp in ['flask', 'django', 'fastapi']:
                    technologies.add('Web Framework')
                elif imp in ['pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch']:
                    technologies.add('Data Science/ML')
                elif imp in ['streamlit', 'dash', 'gradio']:
                    technologies.add('Interactive Apps')
                elif imp in ['matplotlib', 'plotly', 'seaborn']:
                    technologies.add('Data Visualization')

        context_parts.append(f"Languages: {', '.join(languages)}")
        if technologies:
            context_parts.append(f"Technologies: {', '.join(technologies)}")

        # File structure sample
        context_parts.append("\nKey Files:")
        for file_info in project_analysis.get('files', [])[:5]:
            path = file_info.get('path', '')
            analysis = file_info.get('analysis', {})
            lines = analysis.get('lines', 0)
            functions = len(analysis.get('functions', []))
            classes = len(analysis.get('classes', []))
            context_parts.append(f"- {path}: {lines} lines, {functions} functions, {classes} classes")

        # Check for common project indicators
        project_files = [f['path'] for f in project_analysis.get('files', [])]
        if any('app.py' in f or 'main.py' in f for f in project_files):
            context_parts.append("\nEntry Point: Has main application file")
        if any('requirements.txt' in f or 'package.json' in f for f in project_files):
            context_parts.append("Dependencies: Has dependency management")
        if any('test' in f.lower() for f in project_files):
            context_parts.append("Testing: Has test files")

        return '\n'.join(context_parts)

    def _parse_text_response(self, response_text: str, project_analysis: Dict) -> Dict:
        """Parse non-JSON response into structured format"""
        # Fallback parsing if Gemini doesn't return JSON
        lines = response_text.split('\n')

        return {
            "project_description": "An innovative software project with modern architecture and clean code design.",
            "project_type": "Software Application",
            "main_features": ["Core functionality", "User-friendly interface", "Robust architecture"],
            "tech_stack": list(set(
                f.get('analysis', {}).get('language', '') for f in project_analysis.get('files', []) if
                f.get('analysis', {}).get('language'))),
            "target_audience": "Developers and end users",
            "installation_steps": ["Clone the repository", "Install dependencies", "Run the application"],
            "usage_instructions": ["Follow the installation steps", "Run the main application",
                                   "Check documentation for details"],
            "project_structure_explanation": "Well-organized codebase with clear separation of concerns"
        }

    def _generate_fallback_overview(self, project_analysis: Dict, project_path: Path) -> Dict:
        """Generate overview using rule-based approach when AI is not available"""

        # Analyze project characteristics
        languages = set(f.get('analysis', {}).get('language', '') for f in project_analysis.get('files', []))
        languages.discard('')

        total_files = project_analysis.get('total_files', 0)
        total_lines = sum(f.get('analysis', {}).get('lines', 0) for f in project_analysis.get('files', []))

        # Detect project type based on files and imports
        project_files = [f['path'].lower() for f in project_analysis.get('files', [])]
        all_imports = set()
        for f in project_analysis.get('files', []):
            all_imports.update(f.get('analysis', {}).get('imports', []))

        project_type = "Software Application"
        main_features = []
        tech_stack = list(languages)

        # Detect web applications
        if any(imp in all_imports for imp in ['flask', 'django', 'fastapi', 'express']):
            project_type = "Web Application"
            main_features.extend(["Web interface", "API endpoints", "Server-side logic"])

        # Detect CLI tools
        elif any('cli' in f or 'command' in f for f in project_files) or 'argparse' in all_imports:
            project_type = "Command Line Tool"
            main_features.extend(["Command line interface", "Automated tasks", "Configurable options"])

        # Detect data science projects
        elif any(imp in all_imports for imp in ['pandas', 'numpy', 'scikit-learn', 'matplotlib']):
            project_type = "Data Science Project"
            main_features.extend(["Data analysis", "Machine learning", "Visualization"])

        # Detect GUI applications
        elif any(imp in all_imports for imp in ['tkinter', 'pyqt', 'streamlit']):
            project_type = "Desktop/GUI Application"
            main_features.extend(["Graphical interface", "Interactive features", "User-friendly design"])

        # Add common features based on imports
        if 'matplotlib' in all_imports or 'plotly' in all_imports:
            main_features.append("Data visualization")
        if any(imp in all_imports for imp in ['sqlite3', 'sqlalchemy', 'pymongo']):
            main_features.append("Database integration")
        if 'requests' in all_imports:
            main_features.append("API integration")

        return {
            "project_description": f"A {project_type.lower()} built with {', '.join(list(languages)[:2])} featuring modern architecture and clean code design.",
            "project_type": project_type,
            "main_features": main_features[:5] if main_features else ["Core functionality", "Clean architecture",
                                                                      "Extensible design"],
            "tech_stack": tech_stack,
            "target_audience": "Developers and end users looking for reliable software solutions",
            "installation_steps": self._generate_installation_steps(project_path),
            "usage_instructions": self._generate_usage_instructions(project_analysis),
            "project_structure_explanation": f"Well-organized codebase with {total_files} files across {len(languages)} programming languages"
        }

    def _generate_installation_steps(self, project_path: Path) -> List[str]:
        """Generate installation steps based on project files"""
        steps = ["Clone the repository"]

        if (project_path / "requirements.txt").exists():
            steps.extend([
                "Create a virtual environment: `python -m venv venv`",
                "Activate virtual environment: `source venv/bin/activate` (Linux/Mac) or `venv\\Scripts\\activate` (Windows)",
                "Install dependencies: `pip install -r requirements.txt`"
            ])
        elif (project_path / "package.json").exists():
            steps.extend([
                "Install Node.js dependencies: `npm install`"
            ])
        elif (project_path / "pyproject.toml").exists():
            steps.extend([
                "Install the package: `pip install .`"
            ])
        else:
            steps.append("Install required dependencies (check project files for specifics)")

        return steps

    def _generate_usage_instructions(self, project_analysis: Dict) -> List[str]:
        """Generate usage instructions based on project analysis"""
        instructions = []
        project_files = [f['path'] for f in project_analysis.get('files', [])]

        # Look for main entry points
        if any('main.py' in f for f in project_files):
            instructions.append("Run the main application: `python main.py`")
        elif any('app.py' in f for f in project_files):
            instructions.append("Start the application: `python app.py`")
        elif any('cli.py' in f for f in project_files):
            instructions.append("Use the command line interface: `python cli.py --help`")

        # Add common usage patterns
        instructions.extend([
            "Check the documentation for detailed usage examples",
            "Explore the available features and options",
            "Report issues or contribute to the project"
        ])

        return instructions

    def analyze_code_purpose(self, file_path: Path, code_content: str, analysis: Dict) -> str:
        """Enhanced code purpose analysis"""
        if self.gemini_model:
            try:
                prompt = f"""
                Analyze this code file and provide a brief, professional description of its purpose:

                File: {file_path.name}
                Language: {analysis.get('language', 'Unknown')}
                Functions: {', '.join(analysis.get('functions', [])[:5])}
                Classes: {', '.join(analysis.get('classes', [])[:3])}
                Imports: {', '.join(analysis.get('imports', [])[:5])}

                Code preview (first 500 chars):
                {code_content[:500]}

                Provide a concise description of what this file does and its role in the project.
                """

                response = self.gemini_model.generate_content(prompt)
                return response.text.strip()
            except Exception as e:
                print(f"⚠️ Gemini analysis failed for {file_path.name}: {e}")

        # Fallback to original rule-based analysis
        return self._generate_rule_based_description(
            file_path.stem, file_path.suffix,
            analysis.get('functions', []),
            analysis.get('classes', []),
            analysis.get('imports', []),
            []
        )

    def _generate_rule_based_description(self, file_name: str, extension: str, functions: List[str], classes: List[str],
                                         imports: List[str], purposes: List[str]) -> str:
        """Original rule-based description generation"""
        lang_map = {'.py': 'Python', '.js': 'JavaScript', '.ts': 'TypeScript'}
        language = lang_map.get(extension, 'Unknown')
        desc_parts = []

        if purposes:
            purpose_desc = {
                'api': 'Handles API endpoints and web requests',
                'database': 'Manages database operations',
                'ui': 'Implements user interface components',
                'testing': 'Contains test cases and utilities',
                'config': 'Manages application configuration',
                'utils': 'Provides utility functions'
            }
            main_purpose = purposes[0]
            desc_parts.append(f"**Purpose**: {purpose_desc.get(main_purpose, 'General purpose code')}")

        if classes and functions:
            desc_parts.append(
                f"**Architecture**: Object-oriented with {len(classes)} class(es) and {len(functions)} function(s)")
        elif classes:
            desc_parts.append(f"**Architecture**: Class-based with {len(classes)} class(es)")
        elif functions:
            desc_parts.append(f"**Architecture**: Functional with {len(functions)} function(s)")

        if imports:
            critical_deps = [imp for imp in imports if
                             not imp.startswith('.') and imp not in ['os', 'sys', 're', 'json']]
            if critical_deps:
                desc_parts.append(f"**Dependencies**: {', '.join([f'`{dep}`' for dep in critical_deps[:5]])}")

        return '\n'.join(desc_parts) or f"**Purpose**: General {language} module"
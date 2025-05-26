from typing import Dict, List
from pathlib import Path
import warnings
try:
    from transformers import pipeline
    HAS_TRANSFORMERS = True
except ImportError:
    HAS_TRANSFORMERS = False

class AIDocumentationEngine:
    def __init__(self):
        self.summarizer = None
        self._initialize_ai_models()

    def _initialize_ai_models(self):
        if HAS_TRANSFORMERS:
            try:
                # Suppress transformers warnings
                warnings.filterwarnings("ignore", category=UserWarning, module="transformers")
                self.summarizer = pipeline(
                    "summarization",
                    model="t5-small",
                    device=-1,
                    framework="pt"
                )
                print("✅ AI summarization model (t5-small) loaded")
            except Exception as e:
                print(f"⚠️ Could not load AI models: {e}")
                self.summarizer = None
        else:
            print("⚠️ Transformers not available. Using rule-based analysis.")

    def analyze_code_purpose(self, file_path: Path, code_content: str, analysis: Dict) -> str:
        file_name = file_path.stem
        extension = file_path.suffix
        functions = analysis.get('functions', [])
        classes = analysis.get('classes', [])
        imports = analysis.get('imports', [])

        purpose_indicators = {
            'api': ['flask', 'fastapi', 'express', 'router', 'endpoint'],
            'database': ['sqlite', 'mysql', 'postgres', 'sqlalchemy'],
            'ui': ['react', 'vue', 'angular', 'tkinter', 'pyqt'],
            'testing': ['test', 'pytest', 'unittest', 'mocha', 'jest'],
            'config': ['config', 'settings', 'environment', 'env'],
            'utils': ['util', 'helper', 'common', 'shared']
        }

        detected_purposes = []
        code_lower = code_content.lower()
        file_lower = file_name.lower()

        for purpose, keywords in purpose_indicators.items():
            if (any(keyword in code_lower for keyword in keywords) or
                    any(keyword in file_lower for keyword in keywords) or
                    any(keyword in imp.lower() for imp in imports for keyword in keywords)):
                detected_purposes.append(purpose)

        if self.summarizer and len(code_content) < 5000:
            try:
                input_length = len(code_content.split())
                max_length = max(20, input_length // 2)
                summary = self.summarizer(
                    code_content[:1000],
                    max_length=max_length,
                    min_length=10,
                    do_sample=False
                )[0]['summary_text']
                return f"**AI Summary**: {summary}\n**Detected Purposes**: {', '.join(detected_purposes) or 'General'}"
            except Exception:
                pass

        return self._generate_rule_based_description(file_name, extension, functions, classes, imports, detected_purposes)

    def _generate_rule_based_description(self, file_name: str, extension: str, functions: List[str], classes: List[str], imports: List[str], purposes: List[str]) -> str:
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
            desc_parts.append(f"**Architecture**: Object-oriented with {len(classes)} class(es) and {len(functions)} function(s)")
        elif classes:
            desc_parts.append(f"**Architecture**: Class-based with {len(classes)} class(es)")
        elif functions:
            desc_parts.append(f"**Architecture**: Functional with {len(functions)} function(s)")

        if imports:
            critical_deps = [imp for imp in imports if not imp.startswith('.') and imp not in ['os', 'sys', 're', 'json']]
            if critical_deps:
                desc_parts.append(f"**Dependencies**: {', '.join([f'`{dep}`' for dep in critical_deps[:5]])}")

        return '\n'.join(desc_parts) or f"**Purpose**: General {language} module"
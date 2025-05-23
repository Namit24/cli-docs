#!/usr/bin/env python3
"""
Smart CLI Documentation Generator with AI-Powered Analysis
A tool to automatically generate intelligent documentation, visual graphs, and project structure
for any codebase using AI/NLP analysis.
"""

import os
import sys
import argparse
import json
from pathlib import Path
from typing import Dict, List, Set, Optional, Any
import re
from datetime import datetime
import subprocess
import tempfile
import base64

# Try importing required libraries
try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    from matplotlib.patches import FancyBboxPatch
    import networkx as nx
    import numpy as np

    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

try:
    from transformers import pipeline, AutoTokenizer, AutoModel
    import torch

    HAS_TRANSFORMERS = True
except ImportError:
    HAS_TRANSFORMERS = False

try:
    import openai

    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False


class AIDocumentationEngine:
    """AI-powered documentation analysis and generation"""

    def __init__(self):
        self.summarizer = None
        self.classifier = None
        self._initialize_ai_models()

    def _initialize_ai_models(self):
        """Initialize AI models for text analysis"""
        try:
            if HAS_TRANSFORMERS:
                # Use lightweight models that work offline
                self.summarizer = pipeline(
                    "summarization",
                    model="facebook/bart-large-cnn",
                    max_length=150,
                    min_length=50,
                    device=-1  # Use CPU
                )
                print("✅ AI summarization model loaded")
            else:
                print("⚠️  Transformers not available. Using rule-based analysis.")
        except Exception as e:
            print(f"⚠️  Could not load AI models: {e}")
            print("📝 Falling back to enhanced rule-based analysis")

    def analyze_code_purpose(self, file_path: Path, code_content: str, analysis: Dict) -> str:
        """Analyze what the code does and generate intelligent description"""

        # Extract meaningful information
        file_name = file_path.stem
        extension = file_path.suffix
        functions = analysis.get('functions', [])
        classes = analysis.get('classes', [])
        imports = analysis.get('imports', [])

        # Rule-based analysis for code purpose
        purpose_indicators = {
            'api': ['flask', 'fastapi', 'express', 'router', 'endpoint', 'request', 'response'],
            'database': ['sqlite', 'mysql', 'postgres', 'mongodb', 'sqlalchemy', 'prisma', 'mongoose'],
            'ui': ['react', 'vue', 'angular', 'tkinter', 'pyqt', 'gtk', 'javafx'],
            'testing': ['test', 'pytest', 'unittest', 'mocha', 'jest', 'spec'],
            'config': ['config', 'settings', 'environment', 'env'],
            'utils': ['util', 'helper', 'common', 'shared'],
            'model': ['model', 'schema', 'entity', 'dto'],
            'service': ['service', 'manager', 'handler', 'processor'],
            'controller': ['controller', 'view', 'endpoint']
        }

        detected_purposes = []
        code_lower = code_content.lower()
        file_lower = file_name.lower()

        for purpose, keywords in purpose_indicators.items():
            if (any(keyword in code_lower for keyword in keywords) or
                    any(keyword in file_lower for keyword in keywords) or
                    any(keyword in imp.lower() for imp in imports for keyword in keywords)):
                detected_purposes.append(purpose)

        # Generate intelligent description
        description = self._generate_description(
            file_name, extension, functions, classes, imports,
            detected_purposes, code_content
        )

        return description

    def _generate_description(self, file_name: str, extension: str,
                              functions: List[str], classes: List[str],
                              imports: List[str], purposes: List[str],
                              code_content: str) -> str:
        """Generate intelligent description based on analysis"""

        lang_map = {
            '.py': 'Python', '.js': 'JavaScript', '.ts': 'TypeScript',
            '.jsx': 'React JSX', '.tsx': 'React TSX', '.java': 'Java',
            '.cpp': 'C++', '.c': 'C', '.cs': 'C#', '.php': 'PHP',
            '.rb': 'Ruby', '.go': 'Go', '.rs': 'Rust'
        }

        language = lang_map.get(extension, 'Unknown')

        # Start building description
        desc_parts = []

        # File purpose
        if purposes:
            purpose_desc = {
                'api': 'Handles API endpoints and web requests',
                'database': 'Manages database operations and data persistence',
                'ui': 'Implements user interface components and interactions',
                'testing': 'Contains test cases and testing utilities',
                'config': 'Manages application configuration and settings',
                'utils': 'Provides utility functions and helper methods',
                'model': 'Defines data models and schemas',
                'service': 'Implements business logic and services',
                'controller': 'Handles request processing and routing'
            }

            main_purpose = purposes[0]
            desc_parts.append(f"**Primary Function**: {purpose_desc.get(main_purpose, 'General purpose code')}")

        # Architecture insights
        if classes and functions:
            desc_parts.append(
                f"**Architecture**: Object-oriented design with {len(classes)} class(es) and {len(functions)} function(s)")
        elif classes:
            desc_parts.append(f"**Architecture**: Class-based structure with {len(classes)} class(es)")
        elif functions:
            desc_parts.append(f"**Architecture**: Functional programming approach with {len(functions)} function(s)")

        # Key components
        key_components = []
        if classes:
            key_components.extend([f"`{cls}`" for cls in classes[:3]])
        if functions:
            important_functions = [f for f in functions if any(keyword in f.lower()
                                                               for keyword in
                                                               ['main', 'init', 'create', 'process', 'handle',
                                                                'execute'])]
            key_components.extend([f"`{func}()`" for func in important_functions[:3]])

        if key_components:
            desc_parts.append(f"**Key Components**: {', '.join(key_components)}")

        # Dependencies
        if imports:
            critical_deps = [imp for imp in imports if not imp.startswith('.') and
                             not any(std in imp for std in ['os', 'sys', 're', 'json', 'datetime'])]
            if critical_deps:
                desc_parts.append(f"**External Dependencies**: {', '.join([f'`{dep}`' for dep in critical_deps[:5]])}")

        # Code complexity analysis
        lines = len(code_content.split('\n'))
        if lines > 500:
            desc_parts.append("**Complexity**: Large, complex module requiring careful maintenance")
        elif lines > 200:
            desc_parts.append("**Complexity**: Medium-sized module with moderate complexity")
        else:
            desc_parts.append("**Complexity**: Compact, focused implementation")

        return '\n'.join(desc_parts)

    def generate_project_summary(self, project_analysis: Dict) -> str:
        """Generate an intelligent project summary"""
        total_files = len(project_analysis.get('files', []))
        languages = set()
        total_lines = 0
        all_purposes = []

        for file_info in project_analysis.get('files', []):
            analysis = file_info.get('analysis', {})
            languages.add(analysis.get('language', 'Unknown'))
            total_lines += analysis.get('lines', 0)
            purposes = file_info.get('purposes', [])
            all_purposes.extend(purposes)

        # Determine project type
        purpose_counts = {}
        for purpose in all_purposes:
            purpose_counts[purpose] = purpose_counts.get(purpose, 0) + 1

        project_type = "General Application"
        if purpose_counts:
            main_purpose = max(purpose_counts.keys(), key=lambda x: purpose_counts[x])
            project_types = {
                'api': 'Web API/Backend Service',
                'ui': 'User Interface Application',
                'database': 'Data Management System',
                'testing': 'Testing Suite',
                'utils': 'Utility Library'
            }
            project_type = project_types.get(main_purpose, "General Application")

        summary = f"""
## 🔍 Project Intelligence Summary

**Project Type**: {project_type}
**Languages**: {', '.join(sorted(languages))}
**Scale**: {total_files} files, {total_lines:,} lines of code
**Architecture**: {self._analyze_architecture(project_analysis)}

### 📊 Component Distribution
"""

        if purpose_counts:
            for purpose, count in sorted(purpose_counts.items(), key=lambda x: x[1], reverse=True):
                percentage = (count / len(all_purposes)) * 100
                summary += f"- **{purpose.title()}**: {count} files ({percentage:.1f}%)\n"

        return summary

    def _analyze_architecture(self, project_analysis: Dict) -> str:
        """Analyze overall project architecture"""
        total_classes = sum(len(f.get('analysis', {}).get('classes', []))
                            for f in project_analysis.get('files', []))
        total_functions = sum(len(f.get('analysis', {}).get('functions', []))
                              for f in project_analysis.get('files', []))

        if total_classes > total_functions * 0.3:
            return "Object-Oriented with strong class hierarchy"
        elif total_functions > total_classes * 3:
            return "Functional/Procedural programming style"
        else:
            return "Mixed architectural patterns"


class VisualGraphGenerator:
    """Generate visual graphs and diagrams"""

    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        if not HAS_MATPLOTLIB:
            print("⚠️  matplotlib not available. Install with: pip install matplotlib networkx")

    def create_project_structure_graph(self, project_analysis: Dict, project_name: str) -> str:
        """Create visual project structure graph"""
        if not HAS_MATPLOTLIB:
            return "matplotlib not available"

        fig, ax = plt.subplots(1, 1, figsize=(16, 12))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')

        # Title
        fig.suptitle(f'{project_name} - Project Structure', fontsize=20, fontweight='bold')

        # Create hierarchical layout
        files_by_lang = {}
        for file_info in project_analysis.get('files', []):
            lang = file_info.get('analysis', {}).get('language', 'Unknown')
            if lang not in files_by_lang:
                files_by_lang[lang] = []
            files_by_lang[lang].append(file_info)

        colors = plt.cm.Set3(np.linspace(0, 1, len(files_by_lang)))
        y_pos = 9

        for i, (lang, files) in enumerate(files_by_lang.items()):
            # Language header
            lang_box = FancyBboxPatch((0.5, y_pos - 0.3), 2, 0.6,
                                      boxstyle="round,pad=0.1",
                                      facecolor=colors[i],
                                      edgecolor='black', linewidth=2)
            ax.add_patch(lang_box)
            ax.text(1.5, y_pos, lang, ha='center', va='center',
                    fontsize=14, fontweight='bold')

            # Files
            x_pos = 3.5
            for j, file_info in enumerate(files[:6]):  # Limit to 6 files per language
                file_path = file_info.get('path', 'unknown')
                analysis = file_info.get('analysis', {})

                # File box
                file_box = FancyBboxPatch((x_pos, y_pos - 0.25), 1.2, 0.5,
                                          boxstyle="round,pad=0.05",
                                          facecolor='lightblue',
                                          edgecolor='navy', linewidth=1)
                ax.add_patch(file_box)

                # File name
                file_name = Path(file_path).name
                if len(file_name) > 12:
                    file_name = file_name[:9] + "..."
                ax.text(x_pos + 0.6, y_pos, file_name, ha='center', va='center',
                        fontsize=8, fontweight='bold')

                # Metadata
                lines = analysis.get('lines', 0)
                classes = len(analysis.get('classes', []))
                functions = len(analysis.get('functions', []))

                ax.text(x_pos + 0.6, y_pos - 0.15, f"{lines}L {classes}C {functions}F",
                        ha='center', va='center', fontsize=6)

                x_pos += 1.4
                if x_pos > 8.5:
                    break

            y_pos -= 1.2
            if y_pos < 1:
                break

        # Save graph
        output_path = self.output_dir / f'{project_name}_structure.png'
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()

        return str(output_path)

    def create_file_dependency_graph(self, file_path: str, analysis: Dict, project_name: str) -> str:
        """Create visual dependency graph for a specific file"""
        if not HAS_MATPLOTLIB:
            return "matplotlib not available"

        # Create network graph
        G = nx.DiGraph()

        file_name = Path(file_path).stem
        G.add_node(file_name, node_type='main', color='red')

        # Add imports as nodes
        imports = analysis.get('imports', [])
        for imp in imports[:10]:  # Limit to 10 imports
            clean_imp = imp.split('.')[-1] if '.' in imp else imp
            G.add_node(clean_imp, node_type='import', color='lightblue')
            G.add_edge(clean_imp, file_name)

        # Add classes and functions
        classes = analysis.get('classes', [])
        functions = analysis.get('functions', [])

        for cls in classes[:5]:  # Limit to 5 classes
            G.add_node(cls, node_type='class', color='lightgreen')
            G.add_edge(file_name, cls)

        for func in functions[:8]:  # Limit to 8 functions
            if func not in classes:  # Avoid duplicates
                G.add_node(func, node_type='function', color='lightyellow')
                G.add_edge(file_name, func)

        # Create visualization
        plt.figure(figsize=(14, 10))
        pos = nx.spring_layout(G, k=3, iterations=50)

        # Draw nodes by type
        node_colors = {'main': 'red', 'import': 'lightblue',
                       'class': 'lightgreen', 'function': 'lightyellow'}

        for node_type, color in node_colors.items():
            nodes = [node for node in G.nodes()
                     if G.nodes[node].get('node_type') == node_type]
            if nodes:
                nx.draw_networkx_nodes(G, pos, nodelist=nodes,
                                       node_color=color, node_size=2000, alpha=0.8)

        # Draw edges
        nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True,
                               arrowsize=20, alpha=0.6)

        # Draw labels
        nx.draw_networkx_labels(G, pos, font_size=8, font_weight='bold')

        plt.title(f'Dependency Graph: {file_name}', fontsize=16, fontweight='bold')
        plt.axis('off')

        # Add legend
        legend_elements = [
            plt.Circle((0, 0), 0.1, facecolor='red', label='Main File'),
            plt.Circle((0, 0), 0.1, facecolor='lightblue', label='Imports'),
            plt.Circle((0, 0), 0.1, facecolor='lightgreen', label='Classes'),
            plt.Circle((0, 0), 0.1, facecolor='lightyellow', label='Functions')
        ]
        plt.legend(handles=legend_elements, loc='upper left')

        # Save graph
        output_path = self.output_dir / f'{project_name}_{file_name}_deps.png'
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()

        return str(output_path)

    def create_complexity_heatmap(self, project_analysis: Dict, project_name: str) -> str:
        """Create complexity heatmap for the project"""
        if not HAS_MATPLOTLIB:
            return "matplotlib not available"

        files = project_analysis.get('files', [])
        if not files:
            return "No files to analyze"

        # Prepare data
        file_names = []
        complexity_scores = []
        line_counts = []

        for file_info in files[:20]:  # Limit to 20 files for readability
            path = file_info.get('path', 'unknown')
            analysis = file_info.get('analysis', {})

            file_name = Path(path).stem
            if len(file_name) > 15:
                file_name = file_name[:12] + "..."

            lines = analysis.get('lines', 0)
            classes = len(analysis.get('classes', []))
            functions = len(analysis.get('functions', []))

            # Calculate complexity score
            complexity = (lines * 0.1) + (classes * 5) + (functions * 2)

            file_names.append(file_name)
            complexity_scores.append(complexity)
            line_counts.append(lines)

        # Create heatmap
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

        # Complexity heatmap
        complexity_matrix = np.array(complexity_scores).reshape(-1, 1)
        im1 = ax1.imshow(complexity_matrix, cmap='YlOrRd', aspect='auto')
        ax1.set_yticks(range(len(file_names)))
        ax1.set_yticklabels(file_names)
        ax1.set_xticks([])
        ax1.set_title('Code Complexity Score', fontweight='bold')
        plt.colorbar(im1, ax=ax1)

        # Lines of code heatmap
        lines_matrix = np.array(line_counts).reshape(-1, 1)
        im2 = ax2.imshow(lines_matrix, cmap='Blues', aspect='auto')
        ax2.set_yticks(range(len(file_names)))
        ax2.set_yticklabels(file_names)
        ax2.set_xticks([])
        ax2.set_title('Lines of Code', fontweight='bold')
        plt.colorbar(im2, ax=ax2)

        plt.suptitle(f'{project_name} - Code Metrics', fontsize=16, fontweight='bold')

        # Save graph
        output_path = self.output_dir / f'{project_name}_complexity.png'
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()

        return str(output_path)


class CodeAnalyzer:
    """Enhanced code analyzer with AI integration"""

    SUPPORTED_EXTENSIONS = {
        '.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.cpp', '.c', '.h',
        '.cs', '.php', '.rb', '.go', '.rs', '.kt', '.swift', '.dart',
        '.scala', '.clj', '.hs', '.ml', '.r', '.m', '.sh', '.ps1'
    }

    IGNORE_DIRS = {
        '.venv', 'venv', '.env', 'env', 'node_modules', '.git', '.idea',
        '__pycache__', '.pytest_cache', 'build', 'dist', 'target',
        '.gradle', '.mvn', 'bin', 'obj', '.vs', '.vscode', 'coverage',
        '.nyc_output', 'logs', 'log', '.log', 'temp', 'tmp', '.tmp'
    }

    IGNORE_FILES = {
        '.gitignore', '.env', '.env.local', '.env.development', '.env.production',
        'package-lock.json', 'yarn.lock', 'poetry.lock', 'Pipfile.lock',
        'requirements.txt', 'setup.py', 'setup.cfg', 'pyproject.toml',
        'LICENSE', 'README.md', 'CHANGELOG.md', '.DS_Store'
    }

    def __init__(self, project_path: str):
        self.project_path = Path(project_path).resolve()
        self.project_name = self.project_path.name
        self.ai_engine = AIDocumentationEngine()

    def should_ignore_path(self, path: Path) -> bool:
        """Check if a path should be ignored"""
        for part in path.parts:
            if part in self.IGNORE_DIRS:
                return True

        if path.name in self.IGNORE_FILES:
            return True

        return False

    def get_code_files(self) -> List[Path]:
        """Get all code files in the project"""
        code_files = []

        for root, dirs, files in os.walk(self.project_path):
            root_path = Path(root)
            dirs[:] = [d for d in dirs if d not in self.IGNORE_DIRS]

            for file in files:
                file_path = root_path / file

                if (not self.should_ignore_path(file_path) and
                        file_path.suffix.lower() in self.SUPPORTED_EXTENSIONS):
                    code_files.append(file_path)

        return sorted(code_files)

    def analyze_file(self, file_path: Path) -> Dict:
        """Analyze a single code file with AI enhancement"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            return {'error': f"Could not read file: {str(e)}"}

        # Basic analysis
        lines = content.split('\n')
        analysis = {
            'functions': self._extract_functions(content, file_path.suffix),
            'classes': self._extract_classes(content, file_path.suffix),
            'imports': self._extract_imports(content, file_path.suffix),
            'lines': len(lines),
            'language': self._detect_language(file_path.suffix)
        }

        # AI-powered purpose analysis
        try:
            analysis['ai_description'] = self.ai_engine.analyze_code_purpose(
                file_path, content, analysis
            )
        except Exception as e:
            analysis[
                'ai_description'] = f"Basic analysis: {file_path.name} contains {len(analysis['functions'])} functions and {len(analysis['classes'])} classes."

        return analysis

    def _detect_language(self, extension: str) -> str:
        """Detect programming language from file extension"""
        lang_map = {
            '.py': 'Python', '.js': 'JavaScript', '.ts': 'TypeScript',
            '.jsx': 'React JSX', '.tsx': 'React TSX', '.java': 'Java',
            '.cpp': 'C++', '.c': 'C', '.h': 'C/C++ Header',
            '.cs': 'C#', '.php': 'PHP', '.rb': 'Ruby',
            '.go': 'Go', '.rs': 'Rust', '.kt': 'Kotlin',
            '.swift': 'Swift', '.dart': 'Dart', '.scala': 'Scala',
            '.sh': 'Shell Script', '.ps1': 'PowerShell'
        }
        return lang_map.get(extension.lower(), 'Unknown')

    def _extract_functions(self, content: str, extension: str) -> List[str]:
        """Extract function names from code"""
        functions = []

        if extension == '.py':
            pattern = r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\('
            functions.extend(re.findall(pattern, content))
        elif extension in ['.js', '.ts', '.jsx', '.tsx']:
            patterns = [
                r'function\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(',
                r'const\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*\(',
                r'([a-zA-Z_][a-zA-Z0-9_]*)\s*:\s*function\s*\(',
                r'([a-zA-Z_][a-zA-Z0-9_]*)\s*=>\s*'
            ]
            for pattern in patterns:
                functions.extend(re.findall(pattern, content))
        elif extension == '.java':
            pattern = r'(?:public|private|protected|static|\s)+\s+\w+\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\('
            functions.extend(re.findall(pattern, content))
        elif extension in ['.cpp', '.c', '.h']:
            pattern = r'\w+\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*\)\s*{'
            functions.extend(re.findall(pattern, content))

        return list(set(functions))

    def _extract_classes(self, content: str, extension: str) -> List[str]:
        """Extract class names from code"""
        classes = []

        if extension == '.py':
            pattern = r'class\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*[:\(]'
            classes.extend(re.findall(pattern, content))
        elif extension in ['.js', '.ts', '.jsx', '.tsx']:
            pattern = r'class\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*[{]'
            classes.extend(re.findall(pattern, content))
        elif extension == '.java':
            pattern = r'(?:public|private|protected|\s)*class\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*[{]'
            classes.extend(re.findall(pattern, content))
        elif extension in ['.cpp', '.h']:
            pattern = r'class\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*[{:]'
            classes.extend(re.findall(pattern, content))

        return list(set(classes))

    def _extract_imports(self, content: str, extension: str) -> List[str]:
        """Extract import/include statements"""
        imports = []

        if extension == '.py':
            patterns = [
                r'import\s+([a-zA-Z_][a-zA-Z0-9_.]*)',
                r'from\s+([a-zA-Z_][a-zA-Z0-9_.]*)\s+import'
            ]
            for pattern in patterns:
                imports.extend(re.findall(pattern, content))
        elif extension in ['.js', '.ts', '.jsx', '.tsx']:
            patterns = [
                r'import.*from\s+[\'"]([^\'"]+)[\'"]',
                r'require\s*\(\s*[\'"]([^\'"]+)[\'"]\s*\)'
            ]
            for pattern in patterns:
                imports.extend(re.findall(pattern, content))
        elif extension in ['.cpp', '.c', '.h']:
            pattern = r'#include\s*[<"]([^>"]+)[>"]'
            imports.extend(re.findall(pattern, content))
        elif extension == '.java':
            pattern = r'import\s+([a-zA-Z_][a-zA-Z0-9_.]*);'
            imports.extend(re.findall(pattern, content))

        return list(set(imports))


class EnhancedDocumentationGenerator:
    """Enhanced documentation generator with AI and visual capabilities"""

    def __init__(self, analyzer: CodeAnalyzer):
        self.analyzer = analyzer
        self.visual_generator = VisualGraphGenerator('.')

    def generate_intelligent_docs(self) -> str:
        """Generate AI-powered documentation"""
        print("🤖 Analyzing codebase with AI...")

        code_files = self.analyzer.get_code_files()

        # Prepare project analysis
        project_analysis = {
            'files': [],
            'total_files': len(code_files),
            'project_name': self.analyzer.project_name
        }

        print(f"📂 Processing {len(code_files)} files...")

        for i, file_path in enumerate(code_files):
            print(f"  📄 Analyzing {file_path.name} ({i + 1}/{len(code_files)})")

            analysis = self.analyzer.analyze_file(file_path)
            if 'error' not in analysis:
                rel_path = file_path.relative_to(self.analyzer.project_path)
                project_analysis['files'].append({
                    'path': str(rel_path),
                    'analysis': analysis
                })

        # Generate AI summary
        ai_summary = self.analyzer.ai_engine.generate_project_summary(project_analysis)

        # Build documentation
        doc = f"# {self.analyzer.project_name} - AI-Generated Documentation\n\n"
        doc += f"*Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n"
        doc += ai_summary + "\n\n"

        # Detailed file analysis
        doc += "## 📁 Detailed File Analysis\n\n"

        # Group files by language for better organization
        files_by_lang = {}
        for file_info in project_analysis['files']:
            lang = file_info['analysis']['language']
            if lang not in files_by_lang:
                files_by_lang[lang] = []
            files_by_lang[lang].append(file_info)

        for lang, files in files_by_lang.items():
            doc += f"### {lang} Files\n\n"

            for file_info in files:
                path = file_info['path']
                analysis = file_info['analysis']

                doc += f"#### 📄 `{path}`\n\n"
                doc += f"**Lines of Code**: {analysis['lines']}\n\n"

                # AI-generated description
                if 'ai_description' in analysis:
                    doc += analysis['ai_description'] + "\n\n"

                # Technical details
                if analysis['classes'] or analysis['functions'] or analysis['imports']:
                    doc += "**Technical Details**:\n"

                    if analysis['classes']:
                        doc += f"- **Classes**: {', '.join([f'`{cls}`' for cls in analysis['classes']])}\n"

                    if analysis['functions']:
                        func_list = analysis['functions'][:10]  # Limit to first 10
                        func_str = ', '.join([f'`{func}()`' for func in func_list])
                        if len(analysis['functions']) > 10:
                            func_str += f" *(+{len(analysis['functions']) - 10} more)*"
                        doc += f"- **Functions**: {func_str}\n"

                    if analysis['imports']:
                        imp_list = analysis['imports'][:5]  # Limit to first 5
                        imp_str = ', '.join([f'`{imp}`' for imp in imp_list])
                        if len(analysis['imports']) > 5:
                            imp_str += f" *(+{len(analysis['imports']) - 5} more)*"
                        doc += f"- **Dependencies**: {imp_str}\n"

                doc += "\n---\n\n"

        return doc

    def generate_visual_graphs(self) -> List[str]:
        """Generate visual graphs for the project"""
        print("🎨 Generating visual graphs...")

        if not HAS_MATPLOTLIB:
            print("❌ Cannot generate visual graphs - matplotlib not installed")
            print("💡 Install with: pip install matplotlib networkx")
            return []

        generated_graphs = []

        # 1. Project structure graph
        print("  📊 Creating project structure visualization...")
        code_files = self.analyzer.get_code_files()
        project_analysis = {'files': []}

        for file_path in code_files:
            analysis = self.analyzer.analyze_file(file_path)
            if 'error' not in analysis:
                rel_path = file_path.relative_to(self.analyzer.project_path)
                project_analysis['files'].append({
                    'path': str(rel_path),
                    'analysis': analysis
                })

        structure_graph = self.visual_generator.create_project_structure_graph(
            project_analysis, self.analyzer.project_name
        )
        if structure_graph != "matplotlib not available":
            generated_graphs.append(structure_graph)
            print(f"  ✅ Project structure saved: {structure_graph}")

        # 2. Complexity heatmap
        print("  🔥 Creating complexity heatmap...")
        complexity_graph = self.visual_generator.create_complexity_heatmap(
            project_analysis, self.analyzer.project_name
        )
        if complexity_graph != "matplotlib not available":
            generated_graphs.append(complexity_graph)
            print(f"  ✅ Complexity heatmap saved: {complexity_graph}")

        return generated_graphs

    def generate_file_graph(self, file_path: str) -> str:
        """Generate visual graph for a specific file"""
        print(f"🎯 Generating dependency graph for {file_path}...")

        if not HAS_MATPLOTLIB:
            print("❌ Cannot generate visual graphs - matplotlib not installed")
            return "matplotlib not available"

        target_path = Path(file_path)
        if not target_path.exists():
            target_path = self.analyzer.project_path / file_path

        if not target_path.exists():
            return f"Error: File '{file_path}' not found"

        analysis = self.analyzer.analyze_file(target_path)
        if 'error' in analysis:
            return f"Error analyzing file: {analysis['error']}"

        graph_path = self.visual_generator.create_file_dependency_graph(
            str(target_path), analysis, self.analyzer.project_name
        )

        if graph_path != "matplotlib not available":
            print(f"  ✅ Dependency graph saved: {graph_path}")
            return graph_path

        return "Could not generate graph"


def install_dependencies():
    """Install required dependencies"""
    required_packages = [
        "matplotlib",
        "networkx",
        "numpy",
        "transformers",
        "torch"
    ]

    print("🔧 Installing required dependencies...")
    for package in required_packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"  ✅ {package} installed successfully")
        except subprocess.CalledProcessError:
            print(f"  ❌ Failed to install {package}")

    print("🎉 Installation complete! Please restart the tool.")


def main():
    parser = argparse.ArgumentParser(
        description="Smart CLI Documentation Generator with AI-Powered Analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  doc generate docs /path/to/project          # Generate AI-powered documentation
  doc generate structure /path/to/project     # Generate visual project structure
  doc generate graphs /path/to/file.py       # Generate dependency graph for file
  doc install                                # Install required dependencies
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Generate command
    gen_parser = subparsers.add_parser('generate', help='Generate documentation or graphs')
    gen_parser.add_argument('feature', choices=['docs', 'structure', 'graphs'],
                            help='Feature to generate')
    gen_parser.add_argument('path', help='Path to the project or file')
    gen_parser.add_argument('--output', '-o', help='Output file path (optional)')

    # Install command
    subparsers.add_parser('install', help='Install required dependencies')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    if args.command == 'install':
        install_dependencies()
        return

    if args.command == 'generate':
        if args.feature in ['docs', 'structure']:
            # Project-level commands
            if not os.path.exists(args.path):
                print(f"❌ Error: Path '{args.path}' does not exist")
                sys.exit(1)

            print(f"🚀 Starting {args.feature} generation for: {args.path}")

            analyzer = CodeAnalyzer(args.path)
            generator = EnhancedDocumentationGenerator(analyzer)

            if args.feature == 'docs':
                print("📚 Generating AI-powered documentation...")
                output = generator.generate_intelligent_docs()

                # Also generate visual graphs
                visual_graphs = generator.generate_visual_graphs()

                print("\n" + "=" * 60)
                print("📚 AI-GENERATED DOCUMENTATION")
                print("=" * 60)

                if args.output:
                    with open(args.output, 'w', encoding='utf-8') as f:
                        f.write(output)
                    print(f"📄 Documentation saved to: {args.output}")

                    if visual_graphs:
                        print(f"\n🎨 Visual graphs generated:")
                        for graph in visual_graphs:
                            print(f"  📊 {graph}")
                else:
                    print(output)

                    if visual_graphs:
                        print(f"\n🎨 Visual graphs generated in current directory:")
                        for graph in visual_graphs:
                            print(f"  📊 {Path(graph).name}")

            elif args.feature == 'structure':
                print("🏗️  Generating visual project structure...")
                visual_graphs = generator.generate_visual_graphs()

                print("\n" + "=" * 60)
                print("🏗️  PROJECT STRUCTURE GENERATED")
                print("=" * 60)

                if visual_graphs:
                    print(f"📊 Visual graphs saved:")
                    for graph in visual_graphs:
                        print(f"  🎨 {graph}")
                else:
                    print("❌ Could not generate visual structure")

        elif args.feature == 'graphs':
            # File-level command
            print(f"🎯 Generating dependency graph for: {args.path}")

            # Find project root
            file_path = Path(args.path)
            if file_path.is_file():
                project_path = file_path.parent
            else:
                project_path = file_path

            # Look for project indicators
            while project_path.parent != project_path:
                if any((project_path / indicator).exists() for indicator in
                       ['.git', 'package.json', 'requirements.txt', 'setup.py', 'pyproject.toml']):
                    break
                project_path = project_path.parent

            analyzer = CodeAnalyzer(str(project_path))
            generator = EnhancedDocumentationGenerator(analyzer)

            graph_path = generator.generate_file_graph(args.path)

            print("\n" + "=" * 60)
            print("🎯 DEPENDENCY GRAPH GENERATED")
            print("=" * 60)

            if graph_path and "Error" not in graph_path and "not available" not in graph_path:
                print(f"📊 Graph saved to: {graph_path}")

                if args.output:
                    # Copy to specified output location
                    import shutil
                    shutil.copy2(graph_path, args.output)
                    print(f"📄 Graph also copied to: {args.output}")
            else:
                print(f"❌ {graph_path}")


if __name__ == "__main__":
    main()
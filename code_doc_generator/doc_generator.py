from pathlib import Path
from datetime import datetime
from typing import Dict, List  # Added import
from code_doc_generator.analyzer import CodeAnalyzer  # Adjusted import
from code_doc_generator.ai_engine import AIDocumentationEngine  # Adjusted import
from code_doc_generator.visual_generator import VisualGraphGenerator  # Adjusted import
from typing import Dict,List

class EnhancedDocumentationGenerator:
    # ... (rest of the file remains unchanged)
    def __init__(self, analyzer: CodeAnalyzer):
        self.analyzer = analyzer
        self.ai_engine = AIDocumentationEngine()
        self.visual_generator = VisualGraphGenerator('.')

    def generate_readme(self) -> str:
        print("🤖 Generating README.md...")
        project_analysis = self._analyze_project()
        readme = f"""# {self.analyzer.project_name}

*Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*

## Overview
{self._generate_project_summary(project_analysis)}

## Installation
{self._generate_installation_instructions()}

## Dependencies
{self._generate_dependencies(project_analysis)}

## File Analysis
{self._generate_file_analysis(project_analysis)}

## Visualizations
{self._generate_visualizations(project_analysis)}
"""
        output_path = self.analyzer.project_path / 'README.md'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(readme)
        print(f"📄 README.md saved to: {output_path}")
        return readme

    def _analyze_project(self) -> Dict:
        code_files = self.analyzer.get_code_files()
        project_analysis = {'files': [], 'total_files': len(code_files), 'project_name': self.analyzer.project_name}
        for file_path in code_files:
            analysis = self.analyzer.analyze_file(file_path)
            if 'error' not in analysis:
                analysis['ai_description'] = self.ai_engine.analyze_code_purpose(file_path, self._read_file(file_path), analysis)
                project_analysis['files'].append({
                    'path': str(file_path.relative_to(self.analyzer.project_path)),
                    'analysis': analysis
                })
        return project_analysis

    def _read_file(self, file_path: Path) -> str:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception:
            return ""

    def _generate_project_summary(self, project_analysis: Dict) -> str:
        total_files = len(project_analysis.get('files', []))
        languages = set(f['analysis'].get('language', 'Unknown') for f in project_analysis.get('files', []))
        total_lines = sum(f['analysis'].get('lines', 0) for f in project_analysis.get('files', []))
        purposes = [p for f in project_analysis.get('files', []) for p in f['analysis'].get('ai_description', '').split('**Detected Purposes**: ')[-1].split(', ') if 'General' not in p]

        purpose_counts = {}
        for purpose in purposes:
            purpose_counts[purpose] = purpose_counts.get(purpose, 0) + 1
        main_purpose = max(purpose_counts, key=purpose_counts.get, default='General') if purpose_counts else 'General'
        project_types = {
            'api': 'Web API/Backend Service',
            'ui': 'User Interface Application',
            'database': 'Data Management System',
            'testing': 'Testing Suite',
            'utils': 'Utility Library'
        }
        project_type = project_types.get(main_purpose.lower(), 'General Application')

        summary = f"""**Project Type**: {project_type}
**Languages**: {', '.join(sorted(languages))}
**Scale**: {total_files} files, {total_lines:,} lines of code
**Architecture**: {self._analyze_architecture(project_analysis)}"""
        return summary

    def _analyze_architecture(self, project_analysis: Dict) -> str:
        total_classes = sum(len(f.get('analysis', {}).get('classes', [])) for f in project_analysis.get('files', []))
        total_functions = sum(len(f.get('analysis', {}).get('functions', [])) for f in project_analysis.get('files', []))
        if total_classes > total_functions * 0.3:
            return "Object-Oriented with strong class hierarchy"
        elif total_functions > total_classes * 3:
            return "Functional/Procedural programming style"
        return "Mixed architectural patterns"

    def _generate_installation_instructions(self) -> str:
        build_files = self.analyzer.detect_build_files()
        instructions = []
        for build_file in build_files:
            name = build_file['name']
            if name == 'requirements.txt':
                instructions.append("```bash\npip install -r requirements.txt\n```")
            elif name == 'package.json':
                instructions.append("```bash\nnpm install\n```")
            elif name == 'pyproject.toml':
                instructions.append("```bash\npip install .\n```")
        return '\n'.join(instructions) or "No specific installation instructions detected. Check project documentation."

    def _generate_dependencies(self, project_analysis: Dict) -> str:
        all_imports = set()
        for file_info in project_analysis.get('files', []):
            imports = file_info.get('analysis', {}).get('imports', [])
            all_imports.update(imp for imp in imports if not imp.startswith('.') and imp not in ['os', 'sys', 're', 'json'])
        return '\n'.join([f"- `{imp}`" for imp in sorted(all_imports)[:10]]) or "No external dependencies detected."

    def _generate_file_analysis(self, project_analysis: Dict) -> str:
        files_by_lang = {}
        for file_info in project_analysis.get('files', []):
            lang = file_info['analysis']['language']
            files_by_lang.setdefault(lang, []).append(file_info)

        doc = []
        for lang, files in files_by_lang.items():
            doc.append(f"### {lang} Files")
            for file_info in files:
                path = file_info['path']
                analysis = file_info['analysis']
                doc.append(f"#### `{path}`")
                doc.append(f"**Lines of Code**: {analysis['lines']}")
                if 'ai_description' in analysis:
                    doc.append(analysis['ai_description'])
                if analysis['classes'] or analysis['functions'] or analysis['imports']:
                    doc.append("**Technical Details**:")
                    if analysis['classes']:
                        doc.append(f"- **Classes**: {', '.join([f'`{cls}`' for cls in analysis['classes']])}")
                    if analysis['functions']:
                        func_list = analysis['functions'][:10]
                        func_str = ', '.join([f'`{func}()`' for func in func_list])
                        if len(analysis['functions']) > 10:
                            func_str += f" (+{len(analysis['functions']) - 10} more)"
                        doc.append(f"- **Functions**: {func_str}")
                    if analysis['imports']:
                        imp_list = analysis['imports'][:5]
                        imp_str = ', '.join([f'`{imp}`' for imp in imp_list])
                        if len(analysis['imports']) > 5:
                            imp_str += f" (+{len(analysis['imports']) - 5} more)"
                        doc.append(f"- **Dependencies**: {imp_str}")
                doc.append("\n---")
        return '\n'.join(doc)

    def _generate_visualizations(self, project_analysis: Dict) -> str:
        graphs = []
        structure_graph = self.visual_generator.create_project_structure_graph(project_analysis, self.analyzer.project_name)
        if structure_graph != "matplotlib not available":
            graphs.append(f"- Project Structure: `{structure_graph}`")
        complexity_graph = self.visual_generator.create_complexity_heatmap(project_analysis, self.analyzer.project_name)
        if complexity_graph != "matplotlib not available":
            graphs.append(f"- Complexity Heatmap: `{complexity_graph}`")
        return '\n'.join(graphs) or "No visualizations generated (matplotlib not installed)."

    def generate_file_graphs(self, file_path: str) -> str:
        print(f"🎯 Generating graphs for {file_path}...")
        target_path = Path(file_path)
        if not target_path.exists():
            target_path = self.analyzer.project_path / file_path
        if not target_path.exists():
            return f"Error: File '{file_path}' not found"

        analysis = self.analyzer.analyze_file(target_path)
        if 'error' in analysis:
            return f"Error analyzing file: {analysis['error']}"

        graph_zip = self.visual_generator.create_graph_zip(str(target_path), analysis, self.analyzer.project_name)
        if graph_zip != "matplotlib not available":
            print(f"📊 Graphs saved to: {graph_zip}")
            return graph_zip
        return "Could not generate graphs (matplotlib not installed)."

    def generate_structure(self) -> str:
        print("🏗️ Generating project structure visualization...")
        project_analysis = self._analyze_project()
        structure_graph = self.visual_generator.create_project_structure_graph(project_analysis, self.analyzer.project_name)
        if structure_graph != "matplotlib not available":
            print(f"📊 Structure saved to: {structure_graph}")
            return structure_graph
        return "Could not generate structure (matplotlib not installed)."
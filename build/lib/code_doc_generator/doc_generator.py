from pathlib import Path
from datetime import datetime
from typing import Dict, List
from code_doc_generator.analyzer import CodeAnalyzer
from code_doc_generator.ai_engine import AIDocumentationEngine
from code_doc_generator.visual_generator import VisualGraphGenerator


class EnhancedDocumentationGenerator:
    def __init__(self, analyzer: CodeAnalyzer):
        self.analyzer = analyzer
        self.ai_engine = AIDocumentationEngine()
        self.visual_generator = VisualGraphGenerator('.')

    def generate_readme(self) -> str:
        print("🤖 Generating enhanced README.md with AI...")
        project_analysis = self._analyze_project()

        # Get AI-powered project overview
        ai_overview = self.ai_engine.generate_project_overview(project_analysis, self.analyzer.project_path)

        readme = self._build_comprehensive_readme(project_analysis, ai_overview)

        output_path = self.analyzer.project_path / 'README.md'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(readme)
        print(f"📄 Enhanced README.md saved to: {output_path}")
        return readme

    def _build_comprehensive_readme(self, project_analysis: Dict, ai_overview: Dict) -> str:
        """Build a comprehensive, user-friendly README"""
        project_name = self.analyzer.project_name

        readme_parts = []

        # Header with project name and description
        readme_parts.append(f"# {project_name}")
        readme_parts.append("")
        readme_parts.append(f"**{ai_overview.get('project_type', 'Software Project')}**")
        readme_parts.append("")
        readme_parts.append(ai_overview.get('project_description', 'A well-crafted software project.'))
        readme_parts.append("")

        # Add badges/stats
        total_files = project_analysis.get('total_files', 0)
        languages = set(f.get('analysis', {}).get('language', '') for f in project_analysis.get('files', []))
        languages.discard('')
        total_lines = sum(f.get('analysis', {}).get('lines', 0) for f in project_analysis.get('files', []))

        readme_parts.append("## 📊 Project Stats")
        readme_parts.append("")
        readme_parts.append(f"- **Files**: {total_files}")
        readme_parts.append(f"- **Languages**: {', '.join(sorted(languages))}")
        readme_parts.append(f"- **Lines of Code**: {total_lines:,}")
        readme_parts.append("")

        # Features section
        features = ai_overview.get('main_features', [])
        if features:
            readme_parts.append("## ✨ Features")
            readme_parts.append("")
            for feature in features:
                readme_parts.append(f"- {feature}")
            readme_parts.append("")

        # Tech stack
        tech_stack = ai_overview.get('tech_stack', [])
        if tech_stack:
            readme_parts.append("## 🛠️ Tech Stack")
            readme_parts.append("")
            for tech in tech_stack:
                readme_parts.append(f"- **{tech}**")
            readme_parts.append("")

        # Installation section
        installation_steps = ai_overview.get('installation_steps', [])
        readme_parts.append("## 🚀 Installation")
        readme_parts.append("")
        for i, step in enumerate(installation_steps, 1):
            readme_parts.append(f"{i}. {step}")
        readme_parts.append("")

        # Usage section
        usage_instructions = ai_overview.get('usage_instructions', [])
        readme_parts.append("## 💻 Usage")
        readme_parts.append("")
        for instruction in usage_instructions:
            readme_parts.append(f"- {instruction}")
        readme_parts.append("")

        # Project structure
        structure_explanation = ai_overview.get('project_structure_explanation', '')
        if structure_explanation:
            readme_parts.append("## 📁 Project Structure")
            readme_parts.append("")
            readme_parts.append(structure_explanation)
            readme_parts.append("")

            # Add simplified file tree
            readme_parts.append("```")
            readme_parts.append(self._generate_simple_file_tree(project_analysis))
            readme_parts.append("```")
            readme_parts.append("")

        # Dependencies
        dependencies = self._extract_key_dependencies(project_analysis)
        if dependencies:
            readme_parts.append("## 📦 Key Dependencies")
            readme_parts.append("")
            for dep in dependencies[:10]:  # Show top 10
                readme_parts.append(f"- `{dep}`")
            readme_parts.append("")

        # Contributing section
        readme_parts.append("## 🤝 Contributing")
        readme_parts.append("")
        readme_parts.append("Contributions are welcome! Please feel free to submit a Pull Request.")
        readme_parts.append("")

        # Footer
        target_audience = ai_overview.get('target_audience', '')
        if target_audience:
            readme_parts.append(f"## 👥 Target Audience")
            readme_parts.append("")
            readme_parts.append(target_audience)
            readme_parts.append("")

        readme_parts.append("---")
        readme_parts.append(f"*Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")

        return '\n'.join(readme_parts)

    def _generate_simple_file_tree(self, project_analysis: Dict) -> str:
        """Generate a simplified file tree for README"""
        files = project_analysis.get('files', [])
        if not files:
            return f"{self.analyzer.project_name}/"

        # Group files by directory
        dirs = {}
        for file_info in files:
            path = Path(file_info['path'])
            if len(path.parts) > 1:
                dir_name = path.parts[0]
                if dir_name not in dirs:
                    dirs[dir_name] = []
                dirs[dir_name].append(path.name)
            else:
                if 'root' not in dirs:
                    dirs['root'] = []
                dirs['root'].append(path.name)

        # Build tree
        tree_lines = [f"{self.analyzer.project_name}/"]

        # Root files first
        if 'root' in dirs:
            for file in sorted(dirs['root'])[:5]:  # Limit to 5 files
                tree_lines.append(f"├── {file}")
            del dirs['root']

        # Then directories
        for dir_name, files in sorted(dirs.items())[:5]:  # Limit to 5 dirs
            tree_lines.append(f"├── {dir_name}/")
            for file in sorted(files)[:3]:  # Limit to 3 files per dir
                tree_lines.append(f"│   ├── {file}")
            if len(files) > 3:
                tree_lines.append(f"│   └── ... ({len(files) - 3} more files)")

        return '\n'.join(tree_lines)

    def _extract_key_dependencies(self, project_analysis: Dict) -> List[str]:
        """Extract key dependencies from all files"""
        all_imports = set()
        priority_imports = set()

        for file_info in project_analysis.get('files', []):
            imports = file_info.get('analysis', {}).get('imports', [])
            for imp in imports:
                if not imp.startswith('.') and imp not in ['os', 'sys', 're', 'json', 'typing']:
                    all_imports.add(imp)

                    # Prioritize well-known libraries
                    if imp in ['flask', 'django', 'fastapi', 'streamlit', 'pandas', 'numpy',
                               'matplotlib', 'scikit-learn', 'tensorflow', 'pytorch', 'requests']:
                        priority_imports.add(imp)

        # Return priority imports first, then others
        result = list(priority_imports)
        result.extend([imp for imp in sorted(all_imports) if imp not in priority_imports])
        return result[:15]  # Limit to 15 dependencies

    def _analyze_project(self) -> Dict:
        """Analyze project with enhanced AI descriptions"""
        code_files = self.analyzer.get_code_files()
        project_analysis = {
            'files': [],
            'total_files': len(code_files),
            'project_name': self.analyzer.project_name
        }

        print(f"📊 Analyzing {len(code_files)} files...")

        for i, file_path in enumerate(code_files):
            if i % 5 == 0:  # Progress indicator
                print(f"   Processing file {i + 1}/{len(code_files)}...")

            analysis = self.analyzer.analyze_file(file_path)
            if 'error' not in analysis:
                # Get AI description for code files
                if file_path.suffix in ['.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.cpp']:
                    try:
                        code_content = self._read_file(file_path)
                        analysis['ai_description'] = self.ai_engine.analyze_code_purpose(
                            file_path, code_content, analysis
                        )
                    except Exception as e:
                        print(f"⚠️ Could not analyze {file_path.name}: {e}")
                        analysis['ai_description'] = "Code analysis not available"

                project_analysis['files'].append({
                    'path': str(file_path.relative_to(self.analyzer.project_path)),
                    'analysis': analysis
                })

        return project_analysis

    def _read_file(self, file_path: Path) -> str:
        """Safely read file content"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        except Exception:
            return ""

    # Keep existing methods for backward compatibility
    def generate_file_graphs(self, file_path: str) -> str:
        """Generate graphs for a specific file"""
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
        """Generate project structure"""
        print("🏗️ Generating project structure...")
        project_analysis = self._analyze_project()
        structure_text = self.visual_generator.create_project_structure_text(project_analysis,
                                                                             self.analyzer.project_path)
        return structure_text

    # Legacy methods for compatibility
    def _generate_project_summary(self, project_analysis: Dict) -> str:
        """Legacy method - kept for compatibility"""
        return "Use the new AI-powered overview instead"

    def _analyze_architecture(self, project_analysis: Dict) -> str:
        """Legacy method - kept for compatibility"""
        total_classes = sum(len(f.get('analysis', {}).get('classes', [])) for f in project_analysis.get('files', []))
        total_functions = sum(
            len(f.get('analysis', {}).get('functions', [])) for f in project_analysis.get('files', []))
        if total_classes > total_functions * 0.3:
            return "Object-Oriented with strong class hierarchy"
        elif total_functions > total_classes * 3:
            return "Functional/Procedural programming style"
        return "Mixed architectural patterns"

    def _generate_installation_instructions(self) -> str:
        """Legacy method - kept for compatibility"""
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
        return '\n'.join(instructions) or "No specific installation instructions detected."

    def _generate_dependencies(self, project_analysis: Dict) -> str:
        """Legacy method - kept for compatibility"""
        all_imports = set()
        for file_info in project_analysis.get('files', []):
            imports = file_info.get('analysis', {}).get('imports', [])
            all_imports.update(
                imp for imp in imports if not imp.startswith('.') and imp not in ['os', 'sys', 're', 'json'])
        return '\n'.join([f"- `{imp}`" for imp in sorted(all_imports)[:10]]) or "No external dependencies detected."
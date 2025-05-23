#!/usr/bin/env python3
"""
Smart CLI Documentation Generator
A tool to automatically generate documentation, mermaid charts, and project structure
for any codebase while ignoring boilerplate directories.
"""

import os
import sys
import argparse
import json
from pathlib import Path
from typing import Dict, List, Set, Optional
import re
from datetime import datetime


class CodeAnalyzer:
    """Analyzes code files and extracts meaningful information"""

    # File extensions to analyze
    SUPPORTED_EXTENSIONS = {
        '.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.cpp', '.c', '.h',
        '.cs', '.php', '.rb', '.go', '.rs', '.kt', '.swift', '.dart',
        '.scala', '.clj', '.hs', '.ml', '.r', '.m', '.sh', '.ps1'
    }

    # Directories to ignore
    IGNORE_DIRS = {
        '.venv', 'venv', '.env', 'env', 'node_modules', '.git', '.idea',
        '__pycache__', '.pytest_cache', 'build', 'dist', 'target',
        '.gradle', '.mvn', 'bin', 'obj', '.vs', '.vscode', 'coverage',
        '.nyc_output', 'logs', 'log', '.log', 'temp', 'tmp', '.tmp'
    }

    # Files to ignore
    IGNORE_FILES = {
        '.gitignore', '.env', '.env.local', '.env.development', '.env.production',
        'package-lock.json', 'yarn.lock', 'poetry.lock', 'Pipfile.lock',
        'requirements.txt', 'setup.py', 'setup.cfg', 'pyproject.toml',
        'LICENSE', 'README.md', 'CHANGELOG.md', '.DS_Store'
    }

    def __init__(self, project_path: str):
        self.project_path = Path(project_path).resolve()
        self.project_name = self.project_path.name

    def should_ignore_path(self, path: Path) -> bool:
        """Check if a path should be ignored"""
        # Check if any parent directory is in ignore list
        for part in path.parts:
            if part in self.IGNORE_DIRS:
                return True

        # Check if filename is in ignore list
        if path.name in self.IGNORE_FILES:
            return True

        return False

    def get_code_files(self) -> List[Path]:
        """Get all code files in the project"""
        code_files = []

        for root, dirs, files in os.walk(self.project_path):
            root_path = Path(root)

            # Remove ignored directories from dirs list to prevent walking into them
            dirs[:] = [d for d in dirs if d not in self.IGNORE_DIRS]

            for file in files:
                file_path = root_path / file

                if (not self.should_ignore_path(file_path) and
                        file_path.suffix.lower() in self.SUPPORTED_EXTENSIONS):
                    code_files.append(file_path)

        return sorted(code_files)

    def analyze_file(self, file_path: Path) -> Dict:
        """Analyze a single code file"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            return {
                'error': f"Could not read file: {str(e)}",
                'functions': [],
                'classes': [],
                'imports': [],
                'lines': 0
            }

        lines = content.split('\n')
        analysis = {
            'functions': self._extract_functions(content, file_path.suffix),
            'classes': self._extract_classes(content, file_path.suffix),
            'imports': self._extract_imports(content, file_path.suffix),
            'lines': len(lines),
            'language': self._detect_language(file_path.suffix)
        }

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
            # Python functions
            pattern = r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\('
            functions.extend(re.findall(pattern, content))
        elif extension in ['.js', '.ts', '.jsx', '.tsx']:
            # JavaScript/TypeScript functions
            patterns = [
                r'function\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(',
                r'const\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*\(',
                r'([a-zA-Z_][a-zA-Z0-9_]*)\s*:\s*function\s*\(',
                r'([a-zA-Z_][a-zA-Z0-9_]*)\s*=>\s*'
            ]
            for pattern in patterns:
                functions.extend(re.findall(pattern, content))
        elif extension == '.java':
            # Java methods
            pattern = r'(?:public|private|protected|static|\s)+\s+\w+\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\('
            functions.extend(re.findall(pattern, content))
        elif extension in ['.cpp', '.c', '.h']:
            # C/C++ functions
            pattern = r'\w+\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*\)\s*{'
            functions.extend(re.findall(pattern, content))

        return list(set(functions))  # Remove duplicates

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


class DocumentationGenerator:
    """Generates various types of documentation"""

    def __init__(self, analyzer: CodeAnalyzer):
        self.analyzer = analyzer

    def generate_docs(self) -> str:
        """Generate basic documentation for all files"""
        code_files = self.analyzer.get_code_files()

        doc = f"# {self.analyzer.project_name} - Code Documentation\n\n"
        doc += f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        doc += f"Total files analyzed: {len(code_files)}\n\n"

        # Group files by language
        files_by_lang = {}
        total_lines = 0

        for file_path in code_files:
            analysis = self.analyzer.analyze_file(file_path)
            if 'error' in analysis:
                continue

            lang = analysis['language']
            if lang not in files_by_lang:
                files_by_lang[lang] = []

            rel_path = file_path.relative_to(self.analyzer.project_path)
            files_by_lang[lang].append({
                'path': str(rel_path),
                'analysis': analysis
            })
            total_lines += analysis['lines']

        doc += f"Total lines of code: {total_lines}\n\n"

        # Generate documentation by language
        for lang, files in files_by_lang.items():
            doc += f"## {lang} Files\n\n"

            for file_info in files:
                path = file_info['path']
                analysis = file_info['analysis']

                doc += f"### {path}\n\n"
                doc += f"- **Lines of code:** {analysis['lines']}\n"

                if analysis['classes']:
                    doc += f"- **Classes:** {', '.join(analysis['classes'])}\n"

                if analysis['functions']:
                    doc += f"- **Functions:** {', '.join(analysis['functions'])}\n"

                if analysis['imports']:
                    doc += f"- **Dependencies:** {', '.join(analysis['imports'][:5])}"
                    if len(analysis['imports']) > 5:
                        doc += f" (+{len(analysis['imports']) - 5} more)"
                    doc += "\n"

                doc += "\n"

        return doc

    def generate_structure(self) -> str:
        """Generate project structure"""
        structure = f"# {self.analyzer.project_name} - Project Structure\n\n"
        structure += f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

        structure += "```\n"
        structure += f"{self.analyzer.project_name}/\n"

        # Build tree structure
        code_files = self.analyzer.get_code_files()
        tree = {}

        for file_path in code_files:
            rel_path = file_path.relative_to(self.analyzer.project_path)
            parts = rel_path.parts

            current = tree
            for part in parts[:-1]:
                if part not in current:
                    current[part] = {}
                current = current[part]

            # Add file with metadata
            current[parts[-1]] = self.analyzer.analyze_file(file_path)

        structure += self._format_tree(tree, 1)
        structure += "```\n\n"

        return structure

    def _format_tree(self, tree: Dict, indent: int) -> str:
        """Format tree structure for display"""
        result = ""
        items = sorted(tree.items())

        for i, (name, content) in enumerate(items):
            is_last = i == len(items) - 1
            prefix = "└── " if is_last else "├── "
            result += "│   " * (indent - 1) + prefix + name

            if isinstance(content, dict) and 'language' in content:
                # It's a file
                result += f" ({content['language']}, {content['lines']} lines)"
                if content['classes']:
                    result += f" [Classes: {len(content['classes'])}]"
                if content['functions']:
                    result += f" [Functions: {len(content['functions'])}]"
                result += "\n"
            else:
                # It's a directory
                result += "/\n"
                child_prefix = "    " if is_last else "│   "
                child_result = self._format_tree(content, indent + 1)
                result += child_result

        return result

    def generate_mermaid_graph(self, file_path: str) -> str:
        """Generate mermaid graph for a specific file"""
        target_path = Path(file_path)
        if not target_path.exists():
            # Try relative to project path
            target_path = self.analyzer.project_path / file_path

        if not target_path.exists():
            return f"Error: File '{file_path}' not found"

        analysis = self.analyzer.analyze_file(target_path)
        if 'error' in analysis:
            return f"Error analyzing file: {analysis['error']}"

        mermaid = f"# Mermaid Graph for {target_path.name}\n\n"
        mermaid += "```mermaid\n"
        mermaid += "graph TD\n"

        file_node = f"FILE[{target_path.name}]"
        mermaid += f"    {file_node}\n"

        # Add classes
        for i, class_name in enumerate(analysis['classes']):
            class_node = f"CLASS{i}[{class_name}]"
            mermaid += f"    {class_node}\n"
            mermaid += f"    {file_node} --> {class_node}\n"

            # Add methods for this class (simplified)
            class_functions = [f for f in analysis['functions'] if class_name.lower() in f.lower()]
            for j, func in enumerate(class_functions[:3]):  # Limit to 3 functions per class
                func_node = f"FUNC{i}_{j}[{func}()]"
                mermaid += f"    {func_node}\n"
                mermaid += f"    {class_node} --> {func_node}\n"

        # Add standalone functions
        standalone_functions = [f for f in analysis['functions']
                                if not any(c.lower() in f.lower() for c in analysis['classes'])]

        for i, func in enumerate(standalone_functions[:5]):  # Limit to 5 standalone functions
            func_node = f"SFUNC{i}[{func}()]"
            mermaid += f"    {func_node}\n"
            mermaid += f"    {file_node} --> {func_node}\n"

        # Add imports
        for i, imp in enumerate(analysis['imports'][:3]):  # Limit to 3 imports
            import_node = f"IMP{i}[{imp}]"
            mermaid += f"    {import_node}\n"
            mermaid += f"    {import_node} --> {file_node}\n"

        mermaid += "```\n"

        return mermaid


def main():
    parser = argparse.ArgumentParser(description="Smart CLI Documentation Generator")
    parser.add_argument("command", choices=["generate"], help="Command to execute")
    parser.add_argument("feature", choices=["docs", "structure", "graphs"],
                        help="Feature to generate")
    parser.add_argument("path", help="Path to the project or file")
    parser.add_argument("--output", "-o", help="Output file path (optional)")

    args = parser.parse_args()

    if args.command == "generate":
        if args.feature in ["docs", "structure"]:
            # Project-level commands
            if not os.path.exists(args.path):
                print(f"Error: Path '{args.path}' does not exist")
                sys.exit(1)

            analyzer = CodeAnalyzer(args.path)
            generator = DocumentationGenerator(analyzer)

            if args.feature == "docs":
                output = generator.generate_docs()
                print("📚 Generated documentation:")
                print("=" * 50)
            elif args.feature == "structure":
                output = generator.generate_structure()
                print("🏗️  Generated project structure:")
                print("=" * 50)

            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(output)
                print(f"Output saved to: {args.output}")
            else:
                print(output)

        elif args.feature == "graphs":
            # File-level command
            # For graphs, we need both project path and file path
            # Usage: doc generate graphs <file_path> <project_path>
            # Or we can infer project path from file path

            file_path = args.path

            # Try to find project root by looking for common indicators
            current_path = Path(file_path).parent if os.path.isfile(file_path) else Path(file_path)
            project_path = current_path

            while project_path.parent != project_path:
                if any((project_path / indicator).exists() for indicator in
                       ['.git', 'package.json', 'requirements.txt', 'setup.py', 'pyproject.toml']):
                    break
                project_path = project_path.parent

            analyzer = CodeAnalyzer(str(project_path))
            generator = DocumentationGenerator(analyzer)

            output = generator.generate_mermaid_graph(file_path)
            print("📊 Generated mermaid graph:")
            print("=" * 50)

            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(output)
                print(f"Output saved to: {args.output}")
            else:
                print(output)


if __name__ == "__main__":
    main()
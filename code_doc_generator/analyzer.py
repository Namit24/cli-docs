import os
from pathlib import Path
import re
from typing import List, Dict, Set

class CodeAnalyzer:
    SUPPORTED_EXTENSIONS = {
        '.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.cpp', '.c', '.h',
        '.cs', '.php', '.rb', '.go', '.rs', '.kt', '.swift', '.dart'
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

    def should_ignore_path(self, path: Path) -> bool:
        for part in path.parts:
            if part in self.IGNORE_DIRS:
                return True
        return path.name in self.IGNORE_FILES

    def get_code_files(self) -> List[Path]:
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
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            return {'error': f"Could not read file: {str(e)}"}

        lines = content.split('\n')
        return {
            'functions': self._extract_functions(content, file_path.suffix),
            'classes': self._extract_classes(content, file_path.suffix),
            'imports': self._extract_imports(content, file_path.suffix),
            'lines': len(lines),
            'language': self._detect_language(file_path.suffix)
        }

    def _detect_language(self, extension: str) -> str:
        lang_map = {
            '.py': 'Python', '.js': 'JavaScript', '.ts': 'TypeScript',
            '.jsx': 'React JSX', '.tsx': 'React TSX', '.java': 'Java',
            '.cpp': 'C++', '.c': 'C', '.h': 'C/C++ Header',
            '.cs': 'C#', '.php': 'PHP', '.rb': 'Ruby',
            '.go': 'Go', '.rs': 'Rust', '.kt': 'Kotlin',
            '.swift': 'Swift', '.dart': 'Dart'
        }
        return lang_map.get(extension.lower(), 'Unknown')

    def _extract_functions(self, content: str, extension: str) -> List[str]:
        functions = []
        if extension == '.py':
            pattern = r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\('
            functions.extend(re.findall(pattern, content))
        elif extension in ['.js', '.ts', '.jsx', '.tsx']:
            patterns = [
                r'function\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(',
                r'const\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*\(',
                r'([a-zA-Z_][a-zA-Z0-9_]*)\s*=>\s*'
            ]
            for pattern in patterns:
                functions.extend(re.findall(pattern, content))
        return list(set(functions))

    def _extract_classes(self, content: str, extension: str) -> List[str]:
        classes = []
        if extension == '.py':
            pattern = r'class\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*[:\(]'
            classes.extend(re.findall(pattern, content))
        elif extension in ['.js', '.ts', '.jsx', '.tsx']:
            pattern = r'class\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*[{]'
            classes.extend(re.findall(pattern, content))
        return list(set(classes))

    def _extract_imports(self, content: str, extension: str) -> List[str]:
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
        return list(set(imports))

    def detect_build_files(self) -> List[Dict]:
        build_files = []
        for file_path in self.project_path.glob("**/*"):
            if file_path.name in {'requirements.txt', 'package.json', 'pyproject.toml'}:
                build_files.append({
                    'name': file_path.name,
                    'path': str(file_path.relative_to(self.project_path))
                })
        return build_files
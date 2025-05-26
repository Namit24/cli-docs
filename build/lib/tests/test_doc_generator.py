import unittest
from code_doc_generator.analyzer import CodeAnalyzer
from code_doc_generator.doc_generator import EnhancedDocumentationGenerator

class TestEnhancedDocumentationGenerator(unittest.TestCase):
    def setUp(self):
        self.analyzer = CodeAnalyzer(".")
        self.doc_generator = EnhancedDocumentationGenerator(self.analyzer)

    def test_generate_readme(self):
        readme = self.doc_generator.generate_readme()  # Fixed method name
        self.assertIn(f"# {self.analyzer.project_name}", readme)  # Adjusted to match project name
        self.assertIn("## Overview", readme)
        self.assertIn("## Installation", readme)
        self.assertIn("## Dependencies", readme)
        self.assertIn("## File Analysis", readme)

    def test_generate_project_summary(self):
        project_analysis = {
            "files": [
                {
                    "path": "main.py",
                    "analysis": {
                        "language": "Python",
                        "lines": 100,
                        "ai_description": "**Detected Purposes**: utils"
                    }
                }
            ],  # Fixed closing bracket
            "total_files": 1,
            "project_name": "test_project"
        }
        summary = self.doc_generator._generate_project_summary(project_analysis)
        self.assertIn("Project Type: Utility Library", summary)
        self.assertIn("Languages: Python", summary)
        self.assertIn("Scale: 1 files, 100 lines of code", summary)

if __name__ == "__main__":
    unittest.main()
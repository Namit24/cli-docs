import unittest
from unittest.mock import patch
from code_doc_generator.analyzer import CodeAnalyzer
from code_doc_generator.doc_generator import EnhancedDocumentationGenerator

class TestEnhancedDocumentationGenerator(unittest.TestCase):
    def setUp(self):
        self.analyzer = CodeAnalyzer(".")
        self.doc_generator = EnhancedDocumentationGenerator(self.analyzer)

    @patch('code_doc_generator.doc_generator.AIDocumentationEngine.analyze_code_purpose')
    def test_generate_readme(self, mock_analyze):
        mock_analyze.return_value = "**Purpose**: Mocked purpose"
        readme = self.doc_generator.generate_readme()
        self.assertIn(f"# {self.analyzer.project_name}", readme)
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
            ],
            "total_files": 1,
            "project_name": "test_project"
        }
        summary = self.doc_generator._generate_project_summary(project_analysis)
        print(f"Summary output: {repr(summary)}")  # Keep debug print for now
        self.assertIn("**Project Type**: Utility Library", summary)
        self.assertIn("**Languages**: Python", summary)  # Updated to match Markdown
        self.assertIn("**Scale**: 1 files, 100 lines of code", summary)

if __name__ == "__main__":
    unittest.main()
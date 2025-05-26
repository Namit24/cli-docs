import unittest
from code_doc_generator.analyzer import CodeAnalyzer
from pathlib import Path
from typing import List  # Added for type hints

class TestCodeAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = CodeAnalyzer(".")

    def test_extract_functions_python(self):
        content = "def my_function():\n    pass"
        functions = self.analyzer._extract_functions(content, ".py")
        self.assertEqual(functions, ["my_function"])

    def test_extract_classes_python(self):
        content = "class MyClass:\n    pass"
        classes = self.analyzer._extract_classes(content, ".py")
        self.assertEqual(classes, ["MyClass"])

    def test_detect_language(self):
        self.assertEqual(self.analyzer._detect_language(".py"), "Python")
        self.assertEqual(self.analyzer._detect_language(".js"), "JavaScript")
        self.assertEqual(self.analyzer._detect_language(".xyz"), "Unknown")

    def test_should_ignore_path(self):
        self.assertTrue(self.analyzer.should_ignore_path(Path("node_modules/test.js")))
        self.assertTrue(self.analyzer.should_ignore_path(Path("README.md")))
        self.assertFalse(self.analyzer.should_ignore_path(Path("src/main.py")))

if __name__ == "__main__":
    unittest.main()
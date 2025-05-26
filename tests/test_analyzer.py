import unittest
from code_doc_generator.analyzer import CodeAnalyzer

class TestCodeAnalyzer(unittest.TestCase):
    def test_extract_functions_python(self):
        analyzer = CodeAnalyzer(".")
        content = "def my_function():\n    pass"
        functions = analyzer._extract_functions(content, ".py")
        self.assertEqual(functions, ["my_function"])

if __name__ == "__main__":
    unittest.main()
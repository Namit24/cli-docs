# doc_gen

*Generated on: 2025-05-26 15:57:14*

## Overview
**Project Type**: Testing Suite
**Languages**: Python
**Scale**: 11 files, 772 lines of code
**Architecture**: Functional/Procedural programming style

## Installation
```bash
pip install -r requirements.txt
```
```bash
pip install -r requirements.txt
```

## Dependencies
- `AIDocumentationEngine`
- `CodeAnalyzer`
- `Dict`
- `EnhancedDocumentationGenerator`
- `FancyBboxPatch`
- `Flask`
- `List`
- `Path`
- `VisualGraphGenerator`
- `argparse`

## File Analysis
### Python Files
#### `code_doc_generator\__init__.py`
**Lines of Code**: 7
**AI Summary**: from .analyzer import codeAnalytics from import .ai_engine import AIDocumentationEngine .visual_generator import VisualGraphGenerator .cli import main __version__ = "0.1.0"
**Detected Purposes**: General
**Technical Details**:
- **Dependencies**: `AIDocumentationEngine`, `CodeAnalyzer`, `VisualGraphGenerator`, `EnhancedDocumentationGenerator`, `main`

---
#### `code_doc_generator\ai_engine.py`
**Lines of Code**: 89
**AI Summary**: def __init__(self): self.summarizer = None self._initialize_ai_models . def analyze_code_purpose(self, file_path: Path, code_content: str, analysis: Dict) try: from transformers import pipeline HAS_TRANSFORMERS = False class AIDocumentationEngine .
**Detected Purposes**: api, database, ui, testing, config, utils
**Technical Details**:
- **Classes**: `AIDocumentationEngine`
- **Functions**: `_initialize_ai_models()`, `_generate_rule_based_description()`, `__init__()`, `analyze_code_purpose()`
- **Dependencies**: `transformers`, `pipeline`, `Path`, `Dict`, `typing` (+1 more)

---
#### `code_doc_generator\analyzer.py`
**Lines of Code**: 126
**Purpose**: Implements user interface components
**Architecture**: Object-oriented with 1 class(es) and 9 function(s)
**Dependencies**: `Path`, `typing`, `pathlib`, `List`
**Technical Details**:
- **Classes**: `CodeAnalyzer`
- **Functions**: `get_code_files()`, `detect_build_files()`, `_extract_functions()`, `__init__()`, `_detect_language()`, `should_ignore_path()`, `analyze_file()`, `_extract_imports()`, `_extract_classes()`
- **Dependencies**: `re`, `os`, `Path`, `typing`, `pathlib` (+1 more)

---
#### `code_doc_generator\cli.py`
**Lines of Code**: 54
**AI Summary**: import argparse import sys from pathlib import Path import logging from .analyzer import .doc_generator import EnhancedDocumentationGenerator logging.basicConfig . format='%(asctime)s - %(levelname)s'
**Detected Purposes**: config
**Technical Details**:
- **Functions**: `main()`
- **Dependencies**: `argparse`, `sys`, `CodeAnalyzer`, `Path`, `logging` (+2 more)

---
#### `code_doc_generator\doc_generator.py`
**Lines of Code**: 188
**Purpose**: Contains test cases and utilities
**Architecture**: Object-oriented with 1 class(es) and 12 function(s)
**Dependencies**: `code_doc_generator.visual_generator`, `AIDocumentationEngine`, `CodeAnalyzer`, `VisualGraphGenerator`, `from`
**Technical Details**:
- **Classes**: `EnhancedDocumentationGenerator`
- **Functions**: `__init__()`, `_analyze_project()`, `_generate_file_analysis()`, `generate_file_graphs()`, `_generate_dependencies()`, `generate_structure()`, `_analyze_architecture()`, `_generate_installation_instructions()`, `_read_file()`, `_generate_project_summary()` (+2 more)
- **Dependencies**: `code_doc_generator.visual_generator`, `AIDocumentationEngine`, `CodeAnalyzer`, `VisualGraphGenerator`, `from` (+7 more)

---
#### `code_doc_generator\visual_generator.py`
**Lines of Code**: 219
**Architecture**: Object-oriented with 1 class(es) and 6 function(s)
**Dependencies**: `zipfile`, `matplotlib.patches`, `subprocess`, `tempfile`, `matplotlib.pyplot`
**Technical Details**:
- **Classes**: `VisualGraphGenerator`
- **Functions**: `__init__()`, `extract_plots_from_file()`, `create_complexity_heatmap()`, `create_file_dependency_graph()`, `create_graph_zip()`, `create_project_structure_graph()`
- **Dependencies**: `zipfile`, `matplotlib.patches`, `subprocess`, `tempfile`, `matplotlib.pyplot` (+8 more)

---
#### `test_project\api.py`
**Lines of Code**: 7
**AI Summary**: flask import Flask app . return "OK" from def handle_request(self) class ApiServer . if you're a flak importer, you'll be able to use the app to import it .
**Detected Purposes**: api
**Technical Details**:
- **Classes**: `ApiServer`
- **Functions**: `handle_request()`
- **Dependencies**: `Flask`, `flask`

---
#### `test_project\main.py`
**Lines of Code**: 11
**AI Summary**: import numpy as np import matplotlib.pyplot as plt def plot_data() . x = nr.linspace(0, 10, 100) plt.plot(x, nnp.sin(x))
**Detected Purposes**: General
**Technical Details**:
- **Functions**: `plot_data()`, `process_data()`
- **Dependencies**: `matplotlib.pyplot`, `numpy`

---
#### `tests\__init__.py`
**Lines of Code**: 1
**AI Summary**: a fff f s . fs ft fd fn fl fr fw fp fx fm fq fb .
**Detected Purposes**: General

---
#### `tests\test_analyzer.py`
**Lines of Code**: 31
**AI Summary**: def test_should_ignore_path(self): self.assertTrue(self.analyzer.should_igne_path (self.assad)) def tests_should-ignoring_path: self-assertingTrue . def testing_detect_language("js")
**Detected Purposes**: testing
**Technical Details**:
- **Classes**: `MyClass`, `TestCodeAnalyzer`
- **Functions**: `test_should_ignore_path()`, `test_detect_language()`, `my_function()`, `test_extract_functions_python()`, `setUp()`, `test_extract_classes_python()`
- **Dependencies**: `CodeAnalyzer`, `pathlib`, `Path`, `unittest`, `code_doc_generator.analyzer` (+2 more)

---
#### `tests\test_doc_generator.py`
**Lines of Code**: 39
**AI Summary**: import codeAnalyzer from code_doc_generator.doc_gerator import EnhancedDocumentationGenerator class test . def setUp(self): self.analysiszer = CodeAnAlyzer(".") self.doc-generators = EnhanceddDocumentalationGeneerator(self.ananalyz) def test_geneate_readme(self), readme = self.assertIn(f"#
**Detected Purposes**: testing, utils
**Technical Details**:
- **Classes**: `TestEnhancedDocumentationGenerator`
- **Functions**: `setUp()`, `test_generate_readme()`, `test_generate_project_summary()`
- **Dependencies**: `CodeAnalyzer`, `EnhancedDocumentationGenerator`, `code_doc_generator.doc_generator`, `unittest`, `code_doc_generator.analyzer`

---

## Visualizations
- Project Structure: `doc_gen_structure.png`
- Complexity Heatmap: `doc_gen_complexity.png`

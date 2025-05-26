# doc_gen

*Generated on: 2025-05-26 16:11:38*

## Overview
**Project Type**: Testing Suite
**Languages**: Python
**Scale**: 11 files, 793 lines of code
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
- **Dependencies**: `main`, `CodeAnalyzer`, `AIDocumentationEngine`, `EnhancedDocumentationGenerator`, `VisualGraphGenerator`

---
#### `code_doc_generator\ai_engine.py`
**Lines of Code**: 105
**AI Summary**: pathlib import Path import warnings try: from transformers import pipeline HAS_TRANSFORMERS = False class AIDocumentationEngine: def __init___(self): self.summarizer = None self._initialize_ai_models() .
**Detected Purposes**: api, database, ui, testing, config, utils
**Technical Details**:
- **Classes**: `AIDocumentationEngine`
- **Functions**: `_generate_rule_based_description()`, `_initialize_ai_models()`, `analyze_code_purpose()`, `__init__()`
- **Dependencies**: `transformers`, `pipeline`, `pathlib`, `warnings`, `Dict` (+2 more)

---
#### `code_doc_generator\analyzer.py`
**Lines of Code**: 126
**Purpose**: Implements user interface components
**Architecture**: Object-oriented with 1 class(es) and 9 function(s)
**Dependencies**: `pathlib`, `typing`, `List`, `Path`
**Technical Details**:
- **Classes**: `CodeAnalyzer`
- **Functions**: `_extract_classes()`, `detect_build_files()`, `__init__()`, `_extract_functions()`, `_extract_imports()`, `get_code_files()`, `should_ignore_path()`, `analyze_file()`, `_detect_language()`
- **Dependencies**: `os`, `pathlib`, `re`, `typing`, `List` (+1 more)

---
#### `code_doc_generator\cli.py`
**Lines of Code**: 54
**AI Summary**: import argparse import sys from pathlib import Path import logging from .analyzer import .doc_generator import EnhancedDocumentationGenerator logging.basicConfig . format='%(asctime)s - %(levelname)s'
**Detected Purposes**: config
**Technical Details**:
- **Functions**: `main()`
- **Dependencies**: `logging`, `CodeAnalyzer`, `argparse`, `EnhancedDocumentationGenerator`, `pathlib` (+2 more)

---
#### `code_doc_generator\doc_generator.py`
**Lines of Code**: 188
**Purpose**: Contains test cases and utilities
**Architecture**: Object-oriented with 1 class(es) and 12 function(s)
**Dependencies**: `CodeAnalyzer`, `AIDocumentationEngine`, `code_doc_generator.ai_engine`, `code_doc_generator.analyzer`, `datetime`
**Technical Details**:
- **Classes**: `EnhancedDocumentationGenerator`
- **Functions**: `_read_file()`, `_generate_project_summary()`, `generate_readme()`, `_generate_file_analysis()`, `__init__()`, `generate_structure()`, `_analyze_architecture()`, `_generate_installation_instructions()`, `generate_file_graphs()`, `_generate_visualizations()` (+2 more)
- **Dependencies**: `CodeAnalyzer`, `AIDocumentationEngine`, `code_doc_generator.ai_engine`, `code_doc_generator.analyzer`, `datetime` (+7 more)

---
#### `code_doc_generator\visual_generator.py`
**Lines of Code**: 219
**Architecture**: Object-oriented with 1 class(es) and 6 function(s)
**Dependencies**: `matplotlib.patches`, `zipfile`, `matplotlib.pyplot`, `tempfile`, `subprocess`
**Technical Details**:
- **Classes**: `VisualGraphGenerator`
- **Functions**: `create_file_dependency_graph()`, `__init__()`, `create_complexity_heatmap()`, `create_project_structure_graph()`, `extract_plots_from_file()`, `create_graph_zip()`
- **Dependencies**: `matplotlib.patches`, `zipfile`, `matplotlib.pyplot`, `os`, `tempfile` (+8 more)

---
#### `test_project\api.py`
**Lines of Code**: 7
**AI Summary**: flask import Flask app . return "OK" from def handle_request .
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
- **Functions**: `process_data()`, `plot_data()`
- **Dependencies**: `numpy`, `matplotlib.pyplot`

---
#### `tests\__init__.py`
**Lines of Code**: 1
**AI Summary**: a fff f .
**Detected Purposes**: General

---
#### `tests\test_analyzer.py`
**Lines of Code**: 31
**AI Summary**: def test_should_ignore_path(self): self.assertTrue(self.analyzer.should_igne_path (self.assad)) def tests_should-ignoring_path: self-assertingTrue . def testing_detect_language("js")
**Detected Purposes**: testing
**Technical Details**:
- **Classes**: `TestCodeAnalyzer`, `MyClass`
- **Functions**: `setUp()`, `test_extract_classes_python()`, `test_should_ignore_path()`, `test_extract_functions_python()`, `test_detect_language()`, `my_function()`
- **Dependencies**: `unittest`, `CodeAnalyzer`, `code_doc_generator.analyzer`, `pathlib`, `typing` (+2 more)

---
#### `tests\test_doc_generator.py`
**Lines of Code**: 44
**AI Summary**: def setUp(self): self.analyzer = codeAnalyticzer("") self.doc_generator = EnhancedDocumentationGenerator(self.ananalysiszer) def test_gerate_readme(self), readme . self.assertIn(f"# self analysis.project_name, readme) self .assestin("## Overview", readme (self) self,asser
**Detected Purposes**: testing, utils
**Technical Details**:
- **Classes**: `TestEnhancedDocumentationGenerator`
- **Functions**: `test_generate_project_summary()`, `test_generate_readme()`, `setUp()`
- **Dependencies**: `unittest`, `CodeAnalyzer`, `code_doc_generator.analyzer`, `EnhancedDocumentationGenerator`, `code_doc_generator.doc_generator`

---

## Visualizations
- Project Structure: `doc_gen_structure.png`
- Complexity Heatmap: `doc_gen_complexity.png`

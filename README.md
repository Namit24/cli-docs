# doc_gen

*Generated on: 2025-05-26 16:16:20*

## Overview
**Project Type**: General Application
**Languages**: Python
**Scale**: 11 files, 789 lines of code
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
**Purpose**: Mocked purpose
**Technical Details**:
- **Dependencies**: `VisualGraphGenerator`, `CodeAnalyzer`, `main`, `AIDocumentationEngine`, `EnhancedDocumentationGenerator`

---
#### `code_doc_generator\ai_engine.py`
**Lines of Code**: 104
**Purpose**: Mocked purpose
**Technical Details**:
- **Classes**: `AIDocumentationEngine`
- **Functions**: `_generate_rule_based_description()`, `analyze_code_purpose()`, `_initialize_ai_models()`, `__init__()`
- **Dependencies**: `pathlib`, `Path`, `typing`, `warnings`, `pipeline` (+2 more)

---
#### `code_doc_generator\analyzer.py`
**Lines of Code**: 126
**Purpose**: Mocked purpose
**Technical Details**:
- **Classes**: `CodeAnalyzer`
- **Functions**: `get_code_files()`, `should_ignore_path()`, `__init__()`, `_extract_functions()`, `analyze_file()`, `_extract_imports()`, `detect_build_files()`, `_extract_classes()`, `_detect_language()`
- **Dependencies**: `pathlib`, `re`, `Path`, `typing`, `List` (+1 more)

---
#### `code_doc_generator\cli.py`
**Lines of Code**: 54
**Purpose**: Mocked purpose
**Technical Details**:
- **Functions**: `main()`
- **Dependencies**: `sys`, `pathlib`, `CodeAnalyzer`, `Path`, `argparse` (+2 more)

---
#### `code_doc_generator\doc_generator.py`
**Lines of Code**: 186
**Purpose**: Mocked purpose
**Technical Details**:
- **Classes**: `EnhancedDocumentationGenerator`
- **Functions**: `generate_structure()`, `_analyze_architecture()`, `_generate_file_analysis()`, `_analyze_project()`, `_read_file()`, `__init__()`, `_generate_visualizations()`, `_generate_dependencies()`, `generate_file_graphs()`, `_generate_installation_instructions()` (+2 more)
- **Dependencies**: `VisualGraphGenerator`, `datetime`, `code_doc_generator.analyzer`, `pathlib`, `CodeAnalyzer` (+6 more)

---
#### `code_doc_generator\visual_generator.py`
**Lines of Code**: 219
**Purpose**: Mocked purpose
**Technical Details**:
- **Classes**: `VisualGraphGenerator`
- **Functions**: `create_project_structure_graph()`, `__init__()`, `create_file_dependency_graph()`, `create_complexity_heatmap()`, `extract_plots_from_file()`, `create_graph_zip()`
- **Dependencies**: `matplotlib.pyplot`, `Dict`, `pathlib`, `Path`, `tempfile` (+8 more)

---
#### `test_project\api.py`
**Lines of Code**: 7
**Purpose**: Mocked purpose
**Technical Details**:
- **Classes**: `ApiServer`
- **Functions**: `handle_request()`
- **Dependencies**: `flask`, `Flask`

---
#### `test_project\main.py`
**Lines of Code**: 11
**Purpose**: Mocked purpose
**Technical Details**:
- **Functions**: `process_data()`, `plot_data()`
- **Dependencies**: `matplotlib.pyplot`, `numpy`

---
#### `tests\__init__.py`
**Lines of Code**: 1
**Purpose**: Mocked purpose

---
#### `tests\test_analyzer.py`
**Lines of Code**: 31
**Purpose**: Mocked purpose
**Technical Details**:
- **Classes**: `MyClass`, `TestCodeAnalyzer`
- **Functions**: `my_function()`, `test_extract_classes_python()`, `setUp()`, `test_detect_language()`, `test_extract_functions_python()`, `test_should_ignore_path()`
- **Dependencies**: `code_doc_generator.analyzer`, `pathlib`, `Path`, `CodeAnalyzer`, `typing` (+2 more)

---
#### `tests\test_doc_generator.py`
**Lines of Code**: 43
**Purpose**: Mocked purpose
**Technical Details**:
- **Classes**: `TestEnhancedDocumentationGenerator`
- **Functions**: `test_generate_readme()`, `setUp()`, `test_generate_project_summary()`
- **Dependencies**: `code_doc_generator.analyzer`, `CodeAnalyzer`, `patch`, `unittest.mock`, `code_doc_generator.doc_generator` (+2 more)

---

## Visualizations
- Project Structure: `doc_gen_structure.png`
- Complexity Heatmap: `doc_gen_complexity.png`

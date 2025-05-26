import argparse
from pathlib import Path
from code_doc_generator.analyzer import CodeAnalyzer
from code_doc_generator.doc_generator import EnhancedDocumentationGenerator

def main():
    parser = argparse.ArgumentParser(description="Code Documentation Generator")
    subparser = parser.add_subparsers(dest="command")

    docs_parser = subparser.add_parser("generate", help="Generate documentation")
    docs_parser.add_argument("type", choices=["doc", "structure", "graphs"], help="Type of documentation to generate")
    docs_parser.add_argument("path", help="Path to the project directory or file")

    args = parser.parse_args()

    project_path = Path(args.path).resolve()
    analyzer = CodeAnalyzer(project_path)
    generator = EnhancedDocumentationGenerator(analyzer)

    if args.command == "generate":
        if args.type == "doc":
            result = generator.generate_readme()
            print(f"📝 Generated README: {project_path / 'README.md'}")
        elif args.type == "structure":
            result = generator.generate_structure()
            print(f"🏗️ Project structure:\n{result}")
        elif args.type == "graphs":
            result = generator.generate_file_graphs(args.path)
            print(result)

if __name__ == "__main__":
    main()
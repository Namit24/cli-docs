import argparse
import sys
from pathlib import Path
import logging
from .analyzer import CodeAnalyzer
from .doc_generator import EnhancedDocumentationGenerator

logging.basicConfig(filename='code_doc_generator.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    logging.info("Starting CodeDocGenerator")
    parser = argparse.ArgumentParser(
        description="CodeDocGenerator: AI-powered code documentation and visualization",
        epilog="Examples:\n  code-doc generate docs /path/to/project\n  code-doc generate structure /path/to/project\n  code-doc generate graphs /path/to/file.py",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    gen_parser = subparsers.add_parser('generate', help='Generate documentation or graphs')
    gen_parser.add_argument('feature', choices=['docs', 'structure', 'graphs'], help='Feature to generate')
    gen_parser.add_argument('path', help='Path to project or file')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    if args.command == 'generate':
        project_path = Path(args.path).parent if Path(args.path).is_file() else Path(args.path)
        if not project_path.exists():
            logging.error(f"Path '{args.path}' does not exist")
            print(f"❌ Error: Path '{args.path}' does not exist")
            sys.exit(1)

        analyzer = CodeAnalyzer(str(project_path))
        generator = EnhancedDocumentationGenerator(analyzer)

        if args.feature == 'docs':
            logging.info(f"Generating README.md for {args.path}")
            print(f"🚀 Generating README.md for: {args.path}")
            generator.generate_readme()
        elif args.feature == 'structure':
            logging.info(f"Generating structure for {args.path}")
            result = generator.generate_structure()
            print(f"🏗️ Result: {result}")
        elif args.feature == 'graphs':
            logging.info(f"Generating graphs for {args.path}")
            result = generator.generate_file_graphs(args.path)
            print(f"🎯 Result: {result}")

if __name__ == "__main__":
    main()
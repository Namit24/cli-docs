from setuptools import setup, find_packages

setup(
    name="code_doc_generator",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "matplotlib>=3.5.0",
        "networkx>=2.8.0",
        "numpy>=1.21.0",
        "transformers>=4.20.0; python_version>='3.7'",
        "torch>=1.10.0; python_version>='3.7'"
    ],
    entry_points={
        "console_scripts": [
            "code-doc=code_doc_generator.cli:main"
        ]
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A CLI tool for generating AI-powered code documentation and visualizations",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/code_doc_generator",
    license="MIT",
    python_requires=">=3.6",
)
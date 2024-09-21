from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pead_ai",
    version="0.1.0",
    author="Leonard Adolphs",
    author_email="leonard.adolphs.95@gmail.com",
    description="PEAD AI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/leox1v/pead_ai",  # Replace with your GitHub username
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "streamlit",
        "openai",
        "tiktoken",
        "PyPDF2",
        "pandas",
        "openpyxl",
        "tabulate",
    ],
)
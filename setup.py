from setuptools import setup, find_packages
import subprocess
import sys

def install_spacy_model():
    """Install required spaCy model"""
    try:
        subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
    except subprocess.CalledProcessError:
        print("Warning: Failed to install spaCy model. Please run 'python -m spacy download en_core_web_sm' manually.")

setup(
    name="wikiqa",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "wikipedia>=1.4.0",
        "openai>=1.0.0",
        "anthropic>=0.5.0",
        "together>=0.1.0",
        "networkx>=3.0.0",
        "spacy>=3.0.0",
        "pandas>=2.0.0",
        "numpy>=1.20.0",
        "python-dateutil>=2.8.2",
        "tqdm>=4.65.0",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A powerful Wikipedia QA system with LLM integration",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/wikiqa",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
)

# Install spaCy model after setup
install_spacy_model() 
from setuptools import setup, find_packages

setup(
    name="wikiqa",
    version="0.1.2",
    packages=find_packages(),
    setup_requires=[
        "spacy>=3.0.0",
    ],
    install_requires=[
        "wikipedia>=1.4.0",
        "openai>=1.0.0",
        "anthropic>=0.5.0",
        "together>=0.1.0",
        "spacy>=3.0.0",
        "pandas>=2.0.0",
        "numpy>=1.20.0",
        "python-dateutil>=2.8.2",
        "tqdm>=4.65.0",
    ],
    author="Pawan Kumar Rajpoot",
    author_email="pawan.rajpoot2411@gmail.com",
    description="A powerful Wikipedia QA system with LLM integration",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/pawan2411/WikiQA",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing :: General",
    ],
    python_requires=">=3.8",
    keywords="wikipedia, qa, llm, nlp, artificial intelligence",
    project_urls={
        "Bug Reports": "https://github.com/pawan2411/WikiQA/issues",
        "Source": "https://github.com/pawan2411/WikiQA",
    },
) 

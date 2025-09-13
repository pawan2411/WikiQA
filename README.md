# 🎯 WikiQA
[![PyPI Downloads](https://static.pepy.tech/personalized-badge/wikiqa?period=total&units=INTERNATIONAL_SYSTEM&left_color=BLACK&right_color=GREEN&left_text=downloads)](https://pepy.tech/projects/wikiqa)

A powerful Wikipedia Question Answering system with LLM integration. WikiQA allows you to extract information from Wikipedia articles using natural language questions and various extraction methods.

## ✨ Features

- 🤖 Direct question answering about Wikipedia content
- 🔍 Entity extraction from articles
- 📝 Article summarization with customizable length and focus
- ⏳ Timeline extraction from articles
- 🔌 Support for multiple LLM providers (OpenAI, Anthropic, Together)

## 🚀 Installation

```bash
pip install wikiqa
python -m spacy download en
```

## 🎮 Quick Start

```python
from wikiqa import WikiQA

# Initialize with your preferred LLM provider
qa = WikiQA(
    llm_provider="together",  # or "openai" or "anthropic"
    api_key="your_api_key",
    model="your_model_name"  # optional, defaults to provider's best model
)

# Ask a question about a Wikipedia article
answer, page_url, revision_id = qa.ask(
    "What is the capital of France?",
    article="France"
)
print(f"Answer: {answer}")
print(f"Source: {page_url}")

# Extract specific information
birth_date, page_url, revision_id = qa.extract_entity(
    "Albert Einstein",
    "date of birth"
)
print(f"Birth date: {birth_date}")

# Get a summary
summary, page_url, revision_id = qa.summarize(
    article="Python (programming language)",
    length="paragraph"
)
print(f"Summary: {summary}")

# Extract a timeline
timeline, page_url, revision_id = qa.extract_timeline("World War II")
print(f"Timeline: {timeline.events}")
```

## 🤝 Supported LLM Providers

- 🎨 OpenAI (GPT models)
- 🧠 Anthropic (Claude models)
- 🌟 Together (various open-source models)

## 📋 Requirements

- 🐍 Python 3.8 or higher
- 🌐 Internet connection for Wikipedia access
- 🔑 API key for your chosen LLM provider

## 📄 License

MIT License

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

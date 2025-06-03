# 🎯 WikiQA

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

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/wikiqa&type=Date)](https://star-history.com/#yourusername/wikiqa&Date)

## 📊 Stats

![GitHub stars](https://img.shields.io/github/stars/yourusername/wikiqa?style=social)
![GitHub forks](https://img.shields.io/github/forks/yourusername/wikiqa?style=social)
![GitHub issues](https://img.shields.io/github/issues/yourusername/wikiqa)
![GitHub license](https://img.shields.io/github/license/yourusername/wikiqa)
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue) 
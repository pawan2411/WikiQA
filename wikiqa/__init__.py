"""
WikiQA - A powerful Wikipedia Question Answering system with LLM integration
"""

__version__ = "0.1.0"

from .core import WikiQA
from .llm import LLMProvider
from .utils import WikiPage, Entity, Timeline, Citation

__all__ = [
    "WikiQA",
    "LLMProvider",
    "WikiPage",
    "Entity",
    "Timeline",
    "Citation",
] 
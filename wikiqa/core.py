"""
Core functionality for the WikiQA system
"""

import wikipedia
from typing import List, Dict, Any, Optional, Union, Tuple
from .llm import LLMProvider
from .utils import WikiPage, Entity, Timeline, Citation
import spacy
from datetime import datetime
import json

class WikiQA:
    def __init__(
        self,
        llm_provider: str,
        api_key: str,
        model: str = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        cache_results: bool = True
    ):
        """
        Initialize the WikiQA system.
        
        Args:
            llm_provider: The LLM provider to use ("openai", "claude", or "together")
            api_key: API key for the selected provider
            model: Specific model to use (defaults to provider's best model)
            temperature: Sampling temperature for LLM responses
            max_tokens: Maximum tokens in LLM responses
            cache_results: Whether to cache results for better performance
        """
        self.llm = LLMProvider(
            provider=llm_provider,
            api_key=api_key,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens
        )
        self.cache_results = cache_results
        self.cache = {}
        self.nlp = spacy.load("en_core_web_sm")
    
    def _get_best_page_match(self, page_name: str) -> Tuple[str, str, int]:
        """
        Find the best matching Wikipedia page name for a given search term.
        
        Args:
            page_name: The search term or page name
            
        Returns:
            Tuple[str, str, int]: (page title, page URL, revision ID)
        """
        try:
            # First try direct page access
            page = wikipedia.page(page_name)
            return page.title, page.url, page.revision_id
        except wikipedia.exceptions.DisambiguationError as e:
            # If disambiguation page, use the first option
            page = wikipedia.page(e.options[0])
            return page.title, page.url, page.revision_id
        except wikipedia.exceptions.PageError:
            # If page not found, search and use the first result
            search_results = wikipedia.search(page_name, results=1)
            if search_results:
                page = wikipedia.page(search_results[0])
                return page.title, page.url, page.revision_id
            raise ValueError(f"No Wikipedia page found for: {page_name}")
        
    def ask(self, question: str, context: str = None, article: str = None) -> Tuple[str, str, int]:
        """
        Ask a direct question about Wikipedia content or a specific Wikipedia article.
        
        Args:
            question: The question to ask
            context: Optional context to provide with the question
            article: Optional Wikipedia article title to use as context
            
        Returns:
            Tuple[str, str, int]: (answer, page URL, revision ID)
        """
        if context:
            prompt = f"Context: {context}\nQuestion: {question}"
            answer = self.llm.generate(prompt)
            return answer, "", 0
        elif article:
            page_name, page_url, revision_id = self._get_best_page_match(article)
            page = wikipedia.page(page_name)
            prompt = f"Context: {page.content[:2000]}\nQuestion: {question}"
            answer = self.llm.generate(prompt)
            return answer, page_url, revision_id
        else:
            prompt = f"Question: {question}"
            answer = self.llm.generate(prompt)
            return answer, "", 0
    
    def extract_entity(self, article: str, entity_type: str) -> Tuple[str, str, int]:
        """
        Extract specific entity information from a Wikipedia article.
        
        Args:
            article: The Wikipedia article title
            entity_type: Type of entity to extract (e.g., "date of birth")
            
        Returns:
            Tuple[str, str, int]: (entity value, page URL, revision ID)
        """
        page_name, page_url, revision_id = self._get_best_page_match(article)
        page = wikipedia.page(page_name)
        prompt = f"Extract only the {entity_type} from this text. Return only the value, no explanation or context: {page.content[:1000]}"
        entity_value = self.llm.generate(prompt).strip()
        return entity_value, page_url, revision_id
    
    def summarize(
        self,
        article: str = None,
        length: str = "paragraph",
        focus: str = None,
        context: str = None
    ) -> Tuple[str, str, int]:
        """
        Generate a summary of a Wikipedia article or provided context.
        
        Args:
            article: Optional Wikipedia article title
            length: Length of summary ("tweet", "paragraph", or "executive")
            focus: Optional specific aspect to focus on
            context: Optional context to summarize (overrides article if provided)
            
        Returns:
            Tuple[str, str, int]: (summary, page URL, revision ID)
        """
        if context:
            content = context
            prompt = f"Summarize this text in {length} format"
            if focus:
                prompt += f", focusing on {focus}"
            prompt += f": {content[:2000]}"
            summary = self.llm.generate(prompt)
            return summary, "", 0
        elif article:
            page_name, page_url, revision_id = self._get_best_page_match(article)
            page = wikipedia.page(page_name)
            content = page.content
            prompt = f"Summarize this text in {length} format"
            if focus:
                prompt += f", focusing on {focus}"
            prompt += f": {content[:2000]}"
            summary = self.llm.generate(prompt)
            return summary, page_url, revision_id
        else:
            raise ValueError("Either 'context' or 'article' must be provided for summarization.")
    
    def extract_timeline(self, article: str) -> Tuple[Timeline, str, int]:
        """
        Extract chronological events from an article.
        
        Args:
            article: The Wikipedia article title
            
        Returns:
            Tuple[Timeline, str, int]: (timeline, page URL, revision ID)
        """
        page_name, page_url, revision_id = self._get_best_page_match(article)
        page = wikipedia.page(page_name)
        prompt = f"Extract a chronological timeline of events from this text: {page.content}"
        events = self.llm.generate(prompt)
        
        timeline = Timeline(
            events=events,
            source=page_url,
            last_updated=revision_id
        )
        return timeline, page_url, revision_id 
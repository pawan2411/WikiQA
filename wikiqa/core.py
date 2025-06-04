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

class WikiQAError(Exception):
    """Base exception for WikiQA errors"""
    pass

class PageNotFoundError(WikiQAError):
    """Raised when a Wikipedia page cannot be found"""
    pass

class EntityNotFoundError(WikiQAError):
    """Raised when an entity cannot be found in the article"""
    pass

class QuestionAnswerError(WikiQAError):
    """Raised when an answer cannot be generated for a question"""
    pass

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
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            raise WikiQAError("SpaCy model 'en_core_web_sm' not found. Please run: python -m spacy download en_core_web_sm")
    
    def _get_best_page_match(self, page_name: str) -> Tuple[str, str, int]:
        """
        Find the best matching Wikipedia page name for a given search term.
        
        Args:
            page_name: The search term or page name
            
        Returns:
            Tuple[str, str, int]: (page title, page URL, revision ID)
            
        Raises:
            PageNotFoundError: If no matching Wikipedia page is found
        """
        try:
            # First try direct page access
            page = wikipedia.page(page_name)
            return page.title, page.url, page.revision_id
        except wikipedia.exceptions.DisambiguationError as e:
            # If disambiguation page, use the first option
            try:
                page = wikipedia.page(e.options[0])
                return page.title, page.url, page.revision_id
            except wikipedia.exceptions.PageError:
                raise PageNotFoundError(f"Could not resolve disambiguation for '{page_name}'. Available options: {', '.join(e.options[:5])}")
        except wikipedia.exceptions.PageError:
            # If page not found, search and use the first result
            search_results = wikipedia.search(page_name, results=1)
            if search_results:
                try:
                    page = wikipedia.page(search_results[0])
                    return page.title, page.url, page.revision_id
                except wikipedia.exceptions.PageError:
                    raise PageNotFoundError(f"Found page '{search_results[0]}' but could not access its content")
            raise PageNotFoundError(f"No Wikipedia page found for: {page_name}")
        
    def ask(self, question: str, context: str = None, article: str = None) -> Tuple[str, str, int]:
        """
        Ask a direct question about Wikipedia content or a specific Wikipedia article.
        
        Args:
            question: The question to ask
            context: Optional context to provide with the question
            article: Optional Wikipedia article title to use as context
            
        Returns:
            Tuple[str, str, int]: (answer, page URL, revision ID)
            
        Raises:
            QuestionAnswerError: If the question cannot be answered
            PageNotFoundError: If the article cannot be found
        """
        try:
            if context:
                prompt = f"Context: {context}\nQuestion: {question}"
                answer = self.llm.generate(prompt)
                if not answer or answer.strip() == "":
                    raise QuestionAnswerError(f"Could not generate an answer for the question: {question}")
                return answer, "", 0
            elif article:
                page_name, page_url, revision_id = self._get_best_page_match(article)
                page = wikipedia.page(page_name)
                prompt = f"Context: {page.content[:2000]}\nQuestion: {question}"
                answer = self.llm.generate(prompt)
                if not answer or answer.strip() == "":
                    raise QuestionAnswerError(f"Could not find an answer to '{question}' in the article '{article}'")
                return answer, page_url, revision_id
            else:
                prompt = f"Question: {question}"
                answer = self.llm.generate(prompt)
                if not answer or answer.strip() == "":
                    raise QuestionAnswerError(f"Could not generate an answer for the question: {question}")
                return answer, "", 0
        except Exception as e:
            if isinstance(e, (PageNotFoundError, QuestionAnswerError)):
                raise
            raise QuestionAnswerError(f"Error while processing question: {str(e)}")
    
    def extract_entity(self, article: str, entity_type: str) -> Tuple[str, str, int]:
        """
        Extract specific entity information from a Wikipedia article.
        
        Args:
            article: The Wikipedia article title
            entity_type: Type of entity to extract (e.g., "date of birth")
            
        Returns:
            Tuple[str, str, int]: (entity value, page URL, revision ID)
            
        Raises:
            EntityNotFoundError: If the entity cannot be found in the article
            PageNotFoundError: If the article cannot be found
        """
        try:
            page_name, page_url, revision_id = self._get_best_page_match(article)
            page = wikipedia.page(page_name)
            prompt = f"Extract only the {entity_type} from this text. Return only the value, no explanation or context: {page.content[:1000]}"
            entity_value = self.llm.generate(prompt).strip()
            
            if not entity_value or entity_value.lower() in ["not found", "none", "unknown", "n/a"]:
                raise EntityNotFoundError(f"Could not find {entity_type} in the article '{article}'")
                
            return entity_value, page_url, revision_id
        except Exception as e:
            if isinstance(e, (PageNotFoundError, EntityNotFoundError)):
                raise
            raise EntityNotFoundError(f"Error while extracting {entity_type}: {str(e)}")
    
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
            
        Raises:
            PageNotFoundError: If the article cannot be found
            ValueError: If neither article nor context is provided
        """
        try:
            if context:
                content = context
                prompt = f"Summarize this text in {length} format"
                if focus:
                    prompt += f", focusing on {focus}"
                prompt += f": {content[:2000]}"
                summary = self.llm.generate(prompt)
                if not summary or summary.strip() == "":
                    raise ValueError("Could not generate summary from the provided context")
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
                if not summary or summary.strip() == "":
                    raise ValueError(f"Could not generate summary for article '{article}'")
                return summary, page_url, revision_id
            else:
                raise ValueError("Either 'context' or 'article' must be provided for summarization.")
        except Exception as e:
            if isinstance(e, (PageNotFoundError, ValueError)):
                raise
            raise ValueError(f"Error while generating summary: {str(e)}")
    
    def extract_timeline(self, article: str) -> Tuple[Timeline, str, int]:
        """
        Extract chronological events from an article.
        
        Args:
            article: The Wikipedia article title
            
        Returns:
            Tuple[Timeline, str, int]: (timeline, page URL, revision ID)
            
        Raises:
            PageNotFoundError: If the article cannot be found
            ValueError: If no timeline events can be extracted
        """
        try:
            page_name, page_url, revision_id = self._get_best_page_match(article)
            page = wikipedia.page(page_name)
            prompt = f"Extract a chronological timeline of events from this text: {page.content}"
            events = self.llm.generate(prompt)
            
            if not events or events.strip() == "":
                raise ValueError(f"Could not extract timeline events from article '{article}'")
            
            timeline = Timeline(
                events=events,
                source=page_url,
                last_updated=revision_id
            )
            return timeline, page_url, revision_id
        except Exception as e:
            if isinstance(e, (PageNotFoundError, ValueError)):
                raise
            raise ValueError(f"Error while extracting timeline: {str(e)}") 

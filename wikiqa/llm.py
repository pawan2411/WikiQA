"""
LLM provider integration for WikiQA
"""

import openai
import anthropic
import together
from typing import Optional, Dict, Any
from abc import ABC, abstractmethod

class BaseLLMProvider(ABC):
    """Base class for LLM providers"""
    
    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Generate a response from the LLM"""
        pass

class OpenAIProvider(BaseLLMProvider):
    """OpenAI API integration"""
    
    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4",
        temperature: float = 0.7,
        max_tokens: int = 1000
    ):
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
    
    def generate(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
        return response.choices[0].message.content

class ClaudeProvider(BaseLLMProvider):
    """Anthropic Claude API integration"""
    
    def __init__(
        self,
        api_key: str,
        model: str = "claude-3-opus-20240229",
        temperature: float = 0.7,
        max_tokens: int = 1000
    ):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
    
    def generate(self, prompt: str) -> str:
        response = self.client.messages.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
        return response.content[0].text

class TogetherProvider(BaseLLMProvider):
    """Together AI API integration"""
    
    def __init__(
        self,
        api_key: str,
        model: str = "mistralai/Mixtral-8x7B-Instruct-v0.1",
        temperature: float = 0.7,
        max_tokens: int = 1000
    ):
        self.client = together.Together(api_key=api_key)
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
    
    def generate(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
        return response.choices[0].message.content

class LLMProvider:
    """Factory class for LLM providers"""
    
    def __init__(
        self,
        provider: str,
        api_key: str,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ):
        """
        Initialize the LLM provider.
        
        Args:
            provider: The LLM provider to use ("openai", "claude", or "together")
            api_key: API key for the selected provider
            model: Specific model to use (defaults to provider's best model)
            temperature: Sampling temperature for LLM responses
            max_tokens: Maximum tokens in LLM responses
        """
        self.provider = self._get_provider(
            provider,
            api_key,
            model,
            temperature,
            max_tokens
        )
    
    def _get_provider(
        self,
        provider: str,
        api_key: str,
        model: Optional[str],
        temperature: float,
        max_tokens: int
    ) -> BaseLLMProvider:
        """Get the appropriate LLM provider instance"""
        
        providers = {
            "openai": OpenAIProvider,
            "claude": ClaudeProvider,
            "together": TogetherProvider
        }
        
        if provider not in providers:
            raise ValueError(f"Unsupported provider: {provider}")
        
        return providers[provider](
            api_key=api_key,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens
        )
    
    def generate(self, prompt: str) -> str:
        """Generate a response from the LLM"""
        return self.provider.generate(prompt) 
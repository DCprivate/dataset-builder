# Software/DataHarvester/services/transformer_service/src/services/llm_factory.py

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Type, Tuple

import instructor
from anthropic import Anthropic
from openai import OpenAI
from pydantic import BaseModel
from infrastructure.config.llm_config import LLMConfig
from infrastructure.error_handling.exceptions import LLMError, ErrorCode, ErrorSeverity

"""
LLM Provider Factory Module

This module implements a factory pattern for creating and managing different LLM providers
(OpenAI, Anthropic, etc.). It provides a unified interface for LLM interactions while
supporting structured output using Pydantic models.
"""


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""

    @abstractmethod
    def _initialize_client(self) -> Any:
        """Initialize the client for the LLM provider."""
        pass

    @abstractmethod
    def create_completion(
        self, response_model: Type[BaseModel], messages: List[Dict[str, str]], **kwargs
    ) -> Any:
        """Create a completion using the LLM provider."""
        pass


class OpenAIProvider(LLMProvider):
    """OpenAI provider implementation."""

    def __init__(self, settings):
        self.settings = settings
        self.client = self._initialize_client()

    def _initialize_client(self) -> Any:
        return instructor.from_openai(OpenAI(api_key=self.settings.api_key))

    def create_completion(
        self, response_model: Type[BaseModel], messages: List[Dict[str, str]], **kwargs
    ) -> Tuple[BaseModel, Any]:
        completion_params = {
            "model": kwargs.get("model", self.settings.default_model),
            "temperature": kwargs.get("temperature", self.settings.temperature),
            "max_retries": kwargs.get("max_retries", self.settings.max_retries),
            "max_tokens": kwargs.get("max_tokens", self.settings.max_tokens),
            "response_model": response_model,
            "messages": messages,
        }
        return self.client.chat.completions.create_with_completion(**completion_params)


class AnthropicProvider(LLMProvider):
    """Anthropic provider implementation."""

    def __init__(self, settings):
        self.settings = settings
        self.client = self._initialize_client()

    def _initialize_client(self) -> Any:
        return instructor.from_anthropic(Anthropic(api_key=self.settings.api_key))

    def create_completion(
        self, response_model: Type[BaseModel], messages: List[Dict[str, str]], **kwargs
    ) -> Any:
        system_message = next(
            (m["content"] for m in messages if m["role"] == "system"), None
        )
        user_messages = [m for m in messages if m["role"] != "system"]

        completion_params = {
            "model": kwargs.get("model", self.settings.default_model),
            "temperature": kwargs.get("temperature", self.settings.temperature),
            "max_retries": kwargs.get("max_retries", self.settings.max_retries),
            "max_tokens": kwargs.get("max_tokens", self.settings.max_tokens),
            "response_model": response_model,
            "messages": user_messages,
        }
        if system_message:
            completion_params["system"] = system_message

        return self.client.messages.create_with_completion(**completion_params)


class LlamaProvider(LLMProvider):
    """Llama provider implementation."""

    def __init__(self, settings):
        self.settings = settings
        self.client = self._initialize_client()

    def _initialize_client(self) -> Any:
        return instructor.from_openai(
            OpenAI(base_url=self.settings.base_url, api_key=self.settings.api_key),
            mode=instructor.Mode.JSON,
        )

    def create_completion(
        self, response_model: Type[BaseModel], messages: List[Dict[str, str]], **kwargs
    ) -> Any:
        completion_params = {
            "model": kwargs.get("model", self.settings.default_model),
            "temperature": kwargs.get("temperature", self.settings.temperature),
            "max_retries": kwargs.get("max_retries", self.settings.max_retries),
            "max_tokens": kwargs.get("max_tokens", self.settings.max_tokens),
            "response_model": response_model,
            "messages": messages,
        }
        return self.client.chat.completions.create_with_completion(**completion_params)


class DeepSeekProvider(LLMProvider):
    """DeepSeek API provider implementation"""
    def __init__(self, api_key: str, model: str = "deepseek-chat"):
        self.api_key = api_key
        self.model = model
        self.client = self._initialize_client()

    def _initialize_client(self) -> Any:
        """Initialize DeepSeek client"""
        return instructor.patch(OpenAI(
            api_key=self.api_key,
            base_url="https://api.deepseek.com/v1"
        ))

    def create_completion(self, response_model: Type[BaseModel], messages: List[Dict[str, str]], **kwargs) -> Any:
        """Create a completion using DeepSeek's API"""
        try:
            return self.client.chat.completions.create(
                model=self.model,
                response_model=response_model,
                messages=messages,
                **kwargs
            )
        except Exception as e:
            raise LLMError(
                f"DeepSeek completion failed: {str(e)}",
                ErrorCode.LLM_ERROR,
                ErrorSeverity.ERROR,
                details={"model": self.model},
                original_error=e
            )


class LLMFactory:
    """
    Factory class for creating and managing LLM provider instances.

    This class implements the Factory pattern to create appropriate LLM provider
    instances based on the specified provider type. It supports multiple providers
    and handles their initialization and configuration.

    Attributes:
        provider: The name of the LLM provider to use
        settings: Configuration settings for the LLM provider
        llm_provider: The initialized LLM provider instance
    """

    def __init__(self, provider: str):
        self.provider = provider
        self.settings = LLMConfig()
        self.llm_provider = self._create_provider(provider)

    def _create_provider(self, provider_type: str) -> LLMProvider:
        """Create a new LLM provider instance"""
        settings = self.settings
        
        providers = {
            "deepseek": lambda: DeepSeekProvider(
                api_key=settings.deepseek.api_key,
                model=settings.deepseek.model
            ),
            "openai": lambda: OpenAIProvider(settings.openai),
            "anthropic": lambda: AnthropicProvider(settings.anthropic),
        }
        
        if provider_type not in providers:
            raise ValueError(f"Unknown provider type: {provider_type}")
            
        return providers[provider_type]()

    def create_completion(
        self, response_model: Type[BaseModel], messages: List[Dict[str, str]], **kwargs
    ) -> Tuple[BaseModel, Any]:
        """
        Create a completion using the configured LLM provider.

        Args:
            response_model: Pydantic model class defining the expected response structure
            messages: List of message dictionaries containing the conversation
            **kwargs: Additional arguments to pass to the provider

        Returns:
            Tuple containing the parsed response model and raw completion

        Raises:
            TypeError: If response_model is not a Pydantic BaseModel
            ValueError: If the provider is not supported
        """
        if not issubclass(response_model, BaseModel):
            raise TypeError("response_model must be a subclass of pydantic.BaseModel")

        return self.llm_provider.create_completion(response_model, messages, **kwargs)

# Software/DataHarvester/services/data_transformation/src/infrastructure/config/llm_config.py

from typing import Optional
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
import os

load_dotenv()

"""
Configuration for LLM providers.
"""


class LLMProviderSettings(BaseSettings):
    """Base settings for LLM providers."""

    temperature: float = 0.0
    max_tokens: Optional[int] = None
    max_retries: int = 3


class OpenAISettings(LLMProviderSettings):
    """Settings for OpenAI."""

    api_key: str = os.getenv("OPENAI_API_KEY", "")
    default_model: str = "gpt-4o"
    embedding_model: str = "text-embedding-3-small"


class AnthropicSettings(LLMProviderSettings):
    """Settings for Anthropic."""

    api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
    default_model: str = "claude-3-5-sonnet-20240620"
    max_tokens: int = 1024


class LlamaSettings(LLMProviderSettings):
    """Settings for Llama."""

    api_key: str = "key"  # required, but not used
    default_model: str = "llama3"
    base_url: str = "http://localhost:11434/v1"


class DeepSeekSettings(BaseSettings):
    """DeepSeek API settings"""
    api_key: str = os.getenv("DEEPSEEK_API_KEY", "")
    model: str = "deepseek-chat"
    base_url: str = "https://api.deepseek.com/v1"

    class Config:
        env_prefix = 'DEEPSEEK_'


class LLMConfig(BaseSettings):
    """Configuration for all LLM providers."""

    openai: OpenAISettings = OpenAISettings()
    anthropic: AnthropicSettings = AnthropicSettings()
    llama: LlamaSettings = LlamaSettings()
    deepseek: DeepSeekSettings = DeepSeekSettings()

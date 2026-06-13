"""
Configuration Management - Centralized settings for TruthLens AI
Uses Pydantic for validation and environment variable loading
"""

import os
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Category(str, Enum):
    """Available content categories"""
    SCIENCE = "Science"
    POLITICS = "Politics"
    GAMING = "Gaming"


class LLMConfig(BaseModel):
    """Configuration for LLM models"""
    # Using OpenRouter API with free Gemma model
    model: str = Field(default="google/gemma-4-31b-it:free")
    temperature: float = Field(default=0.5, ge=0.0, le=2.0)
    max_tokens: int = Field(default=4096)


class AgentConfigs(BaseModel):
    """Temperature and model settings for each agent"""
    researcher: LLMConfig = Field(default_factory=lambda: LLMConfig(temperature=0.2))
    writer: LLMConfig = Field(default_factory=lambda: LLMConfig(temperature=0.7))
    editor: LLMConfig = Field(default_factory=lambda: LLMConfig(temperature=0.3))


class SearchConfig(BaseModel):
    """Configuration for web search"""
    max_results: int = Field(default=5)  # Reduced to keep content manageable
    include_answer: bool = Field(default=True)
    include_raw_content: bool = Field(default=False)  # Use snippets instead
    max_sources: int = Field(default=5)
    max_content_chars: int = Field(default=3000)  # Truncate for LLM context limits


class WorkflowConfig(BaseModel):
    """Configuration for the workflow"""
    max_iterations: int = Field(default=3, ge=1, le=10)
    content_preview_length: int = Field(default=2000)
    research_preview_length: int = Field(default=1000)


class Settings(BaseModel):
    """Main application settings"""
    # API Keys
    openrouter_api_key: Optional[str] = Field(default=None)
    tavily_api_key: Optional[str] = Field(default=None)

    # Configurations
    llm: AgentConfigs = Field(default_factory=AgentConfigs)
    search: SearchConfig = Field(default_factory=SearchConfig)
    workflow: WorkflowConfig = Field(default_factory=WorkflowConfig)

    # Logging
    log_level: str = Field(default="INFO")

    @classmethod
    def from_env(cls) -> "Settings":
        """Load settings from environment variables"""
        return cls(
            openrouter_api_key=os.getenv("OPENROUTER_API_KEY"),
            tavily_api_key=os.getenv("TAVILY_API_KEY"),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
        )

    def validate_api_keys(self) -> tuple[bool, list[str]]:
        """Validate that required API keys are present"""
        errors = []
        if not self.openrouter_api_key:
            errors.append("OPENROUTER_API_KEY not set")
        if not self.tavily_api_key:
            errors.append("TAVILY_API_KEY not set (web search will be limited)")
        return len(errors) == 0 or (len(errors) == 1 and "TAVILY" in errors[0]), errors


# Global settings instance
settings = Settings.from_env()

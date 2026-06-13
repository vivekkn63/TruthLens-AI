"""
Base Agent - Abstract base class for all agents
Provides common functionality and dependency injection support
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from config import Settings, settings, LLMConfig
from utils.logger import AgentLogger
from utils.retry import with_retry, RetryConfig

# OpenRouter API base URL
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"


class BaseAgent(ABC):
    """
    Abstract base class for all TruthLens agents.

    Provides:
    - LLM initialization with dependency injection
    - Common prompt handling
    - Logging infrastructure
    - Retry logic for API calls
    """

    # Override in subclasses
    AGENT_NAME: str = "base"
    AGENT_ICON: str = "🤖"

    def __init__(
        self,
        llm: Optional[ChatOpenAI] = None,
        llm_config: Optional[LLMConfig] = None,
        app_settings: Optional[Settings] = None,
    ):
        """
        Initialize the agent.

        Args:
            llm: Optional pre-configured LLM (for testing/injection)
            llm_config: Optional LLM configuration override
            app_settings: Optional settings override
        """
        self._settings = app_settings or settings
        self._llm_config = llm_config or self._get_default_llm_config()
        self._llm = llm or self._create_llm()
        self._logger = AgentLogger(self.AGENT_NAME, self.AGENT_ICON)
        self._prompts = self._load_prompts()

    @abstractmethod
    def _get_default_llm_config(self) -> LLMConfig:
        """Get the default LLM configuration for this agent type"""
        pass

    @abstractmethod
    def _load_prompts(self) -> Dict[str, str]:
        """Load category-specific prompts for this agent"""
        pass

    def _create_llm(self) -> ChatOpenAI:
        """Create the OpenRouter LLM using OpenAI-compatible interface"""
        return ChatOpenAI(
            model=self._llm_config.model,
            openai_api_key=self._settings.openrouter_api_key,
            openai_api_base=OPENROUTER_BASE_URL,
            temperature=self._llm_config.temperature,
            max_tokens=self._llm_config.max_tokens,
            default_headers={
                "HTTP-Referer": "https://truthlens.ai",
                "X-Title": "TruthLens AI",
            },
        )

    def get_system_prompt(self, category: str) -> str:
        """
        Get the appropriate system prompt for a category.

        Args:
            category: Content category (Science, Politics, Gaming)

        Returns:
            System prompt string
        """
        category_lower = category.lower()
        default_prompt = self._prompts.get("default", "")
        return self._prompts.get(category_lower, default_prompt)

    @with_retry(config=RetryConfig(max_attempts=3, base_delay=1.0))
    def _invoke_llm(self, prompt: str, system_prompt: str = "") -> str:
        """
        Invoke the LLM with retry logic.

        Args:
            prompt: The user prompt to send to the LLM
            system_prompt: Optional system prompt

        Returns:
            LLM response content
        """
        messages = []
        if system_prompt:
            messages.append(SystemMessage(content=system_prompt))
        messages.append(HumanMessage(content=prompt))

        response = self._llm.invoke(messages)
        return response.content

    def _invoke_llm_safe(self, prompt: str, system_prompt: str = "", fallback: str = "") -> str:
        """
        Safely invoke the LLM with fallback on failure.

        Args:
            prompt: The user prompt to send to the LLM
            system_prompt: Optional system prompt
            fallback: Fallback value if invocation fails

        Returns:
            LLM response or fallback
        """
        try:
            return self._invoke_llm(prompt, system_prompt)
        except Exception as e:
            self._logger.error(f"LLM invocation failed: {e}")
            return fallback

    @property
    def logger(self) -> AgentLogger:
        """Get the agent's logger"""
        return self._logger

    @property
    def llm(self) -> ChatOpenAI:
        """Get the agent's LLM"""
        return self._llm

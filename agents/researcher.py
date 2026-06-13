"""Researcher Agent - Conducts web research using Tavily"""

from typing import Optional, Dict, Set
from langchain_openai import ChatOpenAI
from tavily import TavilyClient

from agents.base import BaseAgent
from config import Settings, settings, LLMConfig
from state import AgentState
from prompts.researcher_prompts import (
    RESEARCHER_SCIENCE,
    RESEARCHER_POLITICS,
    RESEARCHER_GAMING,
    RESEARCHER_DEFAULT,
)


class ResearcherAgent(BaseAgent):
    """Agent responsible for researching topics using web search"""

    AGENT_NAME = "researcher"
    AGENT_ICON = "🔍"

    def __init__(
        self,
        llm: Optional[ChatOpenAI] = None,
        llm_config: Optional[LLMConfig] = None,
        tavily_client: Optional[TavilyClient] = None,
        app_settings: Optional[Settings] = None,
    ):
        super().__init__(llm, llm_config, app_settings)
        self._tavily = tavily_client or self._create_tavily_client()

    def _get_default_llm_config(self) -> LLMConfig:
        return settings.llm.researcher

    def _load_prompts(self) -> Dict[str, str]:
        return {
            "science": RESEARCHER_SCIENCE,
            "politics": RESEARCHER_POLITICS,
            "gaming": RESEARCHER_GAMING,
            "default": RESEARCHER_DEFAULT,
        }

    def _create_tavily_client(self) -> TavilyClient:
        """Create the Tavily search client"""
        return TavilyClient(api_key=self._settings.tavily_api_key)

    def _search_topic(self, query: str) -> dict:
        """
        Search for information about a topic using Tavily.

        Args:
            query: Search query string

        Returns:
            Search results dictionary
        """
        try:
            search_params = {
                "query": query,
                "max_results": self._settings.search.max_results,
                "include_answer": self._settings.search.include_answer,
                "include_raw_content": self._settings.search.include_raw_content,
            }
            return self._tavily.search(**search_params)
        except Exception as e:
            self.logger.error(f"Search error: {e}")
            return {"results": [], "answer": ""}

    def _process_search_results(self, search_results: dict) -> tuple[str, list[str]]:
        """
        Process search results into structured research content.

        Args:
            search_results: Raw search results from Tavily

        Returns:
            Tuple of (processed content, list of source URLs)
        """
        content_parts = []
        sources = []

        # Add answer summary if available
        if search_results.get("answer"):
            content_parts.append(f"Summary: {search_results['answer']}\n")

        # Process each result
        for result in search_results.get("results", []):
            title = result.get("title", "")
            url = result.get("url", "")
            content_snippet = result.get("content", "")
            raw_content = result.get("raw_content", "")

            if title and (content_snippet or raw_content):
                content_parts.append(f"Source: {title}")
                if url:
                    content_parts.append(f"URL: {url}")
                    sources.append(url)
                content_parts.append(raw_content if raw_content else content_snippet)
                content_parts.append("-" * 80)

        return "\n".join(content_parts), sources

    def _generate_search_queries(self, topic: str, category: str) -> list[str]:
        """
        Generate search queries for comprehensive research.

        Args:
            topic: Research topic
            category: Content category

        Returns:
            List of search queries
        """
        return [
            f"{topic} {category}",
            topic,
            f"recent research {topic}",
            f"latest news {topic}",
        ]

    def _deduplicate_results(self, results: list[dict]) -> list[dict]:
        """
        Remove duplicate results based on URL.

        Args:
            results: List of search result dictionaries

        Returns:
            Deduplicated list of results
        """
        seen_urls: Set[str] = set()
        unique_results = []

        for result in results:
            url = result.get("url")
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_results.append(result)

        return unique_results

    def _build_synthesis_prompt(self, topic: str, category: str, research_content: str) -> str:
        """
        Build the prompt for synthesizing research.

        Args:
            topic: Research topic
            category: Content category
            research_content: Raw research content

        Returns:
            Synthesis prompt string
        """
        return f"""You are synthesizing research ONLY about this specific topic:

TOPIC: {topic}
CATEGORY: {category}

CRITICAL INSTRUCTIONS:
- ONLY include information directly related to "{topic}"
- Do NOT include information about other topics, even if present in the raw data
- Stay strictly focused on the given topic
- If the raw data contains irrelevant information, ignore it completely

RAW RESEARCH DATA:
{research_content}

Create a well-structured research summary about ONLY "{topic}".

Organize into these sections (only include sections relevant to the topic):
1. Topic Overview - What is {topic}?
2. Key Facts and Findings - Specific to {topic}
3. Important Concepts and Terms - Related to {topic}
4. Recent Developments - Latest news about {topic}
5. Multiple Perspectives - Different viewpoints on {topic}
6. Impact and Significance - Why {topic} matters
7. Areas of Uncertainty - What's still unknown about {topic}

REMEMBER: Every sentence must be about "{topic}". Do not deviate."""

    def research(self, state: AgentState) -> AgentState:
        """
        Execute research on the given topic.

        Args:
            state: Current agent state

        Returns:
            Updated agent state with research content
        """
        self.logger.info(f"Starting research on '{state.topic}' in category '{state.category}'")

        # Generate search queries
        search_queries = self._generate_search_queries(state.topic, state.category)

        # Collect all search results
        all_results = []
        all_sources: Set[str] = set()

        for query in search_queries:
            self.logger.step(f"Searching: {query}")
            results = self._search_topic(query)

            if results.get("results"):
                all_results.extend(results["results"])
                all_sources.update(
                    r.get("url") for r in results["results"] if r.get("url")
                )

        # Deduplicate results
        unique_results = self._deduplicate_results(all_results)

        # Process results into structured format
        search_data = {"results": unique_results, "answer": ""}
        research_content, sources = self._process_search_results(search_data)

        # Truncate research content to fit in LLM context window
        max_chars = self._settings.search.max_content_chars
        if len(research_content) > max_chars:
            research_content = research_content[:max_chars] + "\n\n[Content truncated for processing...]"
            self.logger.step(f"Truncated research to {max_chars} chars for LLM")

        # Synthesize research using LLM
        synthesis_prompt = self._build_synthesis_prompt(state.topic, state.category, research_content)
        synthesized_research = self._invoke_llm_safe(
            synthesis_prompt, fallback=research_content
        )

        # Update state
        state.research_content = synthesized_research
        state.research_sources = list(sources)[: self._settings.search.max_sources]
        state.messages.append(
            f"Researcher: Completed research on '{state.topic}' with {len(state.research_sources)} sources"
        )

        self.logger.result("Sources found", len(state.research_sources))
        self.logger.result("Research length", f"{len(synthesized_research)} characters")

        return state

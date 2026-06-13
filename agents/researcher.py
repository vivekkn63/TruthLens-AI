"""
Researcher Agent - Conducts thorough online research using web search
"""

import os
from typing import Any
from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.messages import HumanMessage
from tavily import TavilyClient
from state import AgentState, ResearcherOutput
from prompts.researcher_prompts import (
    RESEARCHER_SCIENCE, RESEARCHER_POLITICS, RESEARCHER_GAMING, RESEARCHER_DEFAULT
)


class ResearcherAgent:
    """Agent responsible for researching topics using web search"""
    
    def __init__(self):
        self.llm = HuggingFaceEndpoint(
            repo_id="meta-llama/Llama-2-7b-chat-hf",
            huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
            temperature=0.2
        )
        self.tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        
        self.prompts = {
            "science": RESEARCHER_SCIENCE,
            "politics": RESEARCHER_POLITICS,
            "gaming": RESEARCHER_GAMING,
        }
    
    def get_system_prompt(self, category: str) -> str:
        """Get appropriate system prompt based on category"""
        category_lower = category.lower()
        return self.prompts.get(category_lower, RESEARCHER_DEFAULT)
    
    def search_topic(self, query: str, include_domains: list[str] = None) -> dict:
        """Search for information about a topic using Tavily"""
        try:
            search_params = {
                "query": query,
                "max_results": 10,
                "include_answer": True,
                "include_raw_content": True
            }
            
            if include_domains:
                search_params["include_domains"] = include_domains
            
            results = self.tavily_client.search(**search_params)
            return results
        except Exception as e:
            print(f"Search error: {e}")
            return {"results": [], "answer": ""}
    
    def process_search_results(self, search_results: dict) -> tuple[str, list[str]]:
        """Process search results into structured research content"""
        content = []
        sources = []
        
        # Add answer summary if available
        if search_results.get("answer"):
            content.append(f"Summary: {search_results['answer']}\n")
        
        # Process each result
        for result in search_results.get("results", []):
            title = result.get("title", "")
            url = result.get("url", "")
            content_snippet = result.get("content", "")
            raw_content = result.get("raw_content", "")
            
            if title and (content_snippet or raw_content):
                content.append(f"Source: {title}")
                if url:
                    content.append(f"URL: {url}")
                    sources.append(url)
                content.append(raw_content if raw_content else content_snippet)
                content.append("-" * 80)
        
        return "\n".join(content), sources
    
    def research(self, state: AgentState) -> AgentState:
        """Execute research on the given topic"""
        print(f"\n🔍 RESEARCHER: Starting research on '{state.topic}' in category '{state.category}'")
        
        # Get category-specific search hints
        category_lower = state.category.lower()
        
        search_queries = [
            f"{state.topic} {state.category}",
            state.topic,
            f"recent research {state.topic}",
            f"latest news {state.topic}",
        ]
        
        all_search_results = {"results": [], "answer": ""}
        all_sources = set()
        
        # Conduct multiple searches for comprehensive research
        for query in search_queries:
            print(f"  Searching: {query}")
            results = self.search_topic(query)
            
            if results.get("results"):
                all_search_results["results"].extend(results["results"])
                if results.get("answer") and not all_search_results["answer"]:
                    all_search_results["answer"] = results["answer"]
            
            if results.get("results"):
                all_sources.update([r.get("url") for r in results["results"] if r.get("url")])
        
        # Remove duplicates
        seen_urls = set()
        unique_results = []
        for result in all_search_results["results"]:
            url = result.get("url")
            if url not in seen_urls:
                seen_urls.add(url)
                unique_results.append(result)
        
        all_search_results["results"] = unique_results
        
        # Process results into structured format
        research_content, sources = self.process_search_results(all_search_results)
        
        # Use LLM to synthesize and structure the research
        system_prompt = self.get_system_prompt(state.category)
        
        synthesis_prompt = f"""Based on the following raw research data, create a well-structured research summary about: {state.topic}

RAW RESEARCH DATA:
{research_content}

Please organize this into:
1. Topic overview
2. Key facts and findings
3. Important concepts and terms (with explanations)
4. Recent developments
5. Multiple perspectives (if applicable)
6. Impact and significance
7. Areas of uncertainty or ongoing research

Make it comprehensive and well-organized."""
        
        try:
            messages = [
                HumanMessage(content=synthesis_prompt)
            ]
            
            response = self.llm.invoke(messages)
            synthesized_research = response.content
        except Exception as e:
            print(f"Synthesis error: {e}")
            synthesized_research = research_content
        
        state.research_content = synthesized_research
        state.research_sources = list(sources)[:10]  # Top 10 sources
        state.messages.append(f"Researcher: Completed research on '{state.topic}' with {len(state.research_sources)} sources")
        
        print(f"  ✓ Research completed with {len(state.research_sources)} sources")
        print(f"  ✓ Research length: {len(synthesized_research)} characters")
        
        return state

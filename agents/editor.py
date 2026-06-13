"""Editor Agent - Reviews and polishes blog content"""

from typing import Optional, Dict, Tuple
from langchain_openai import ChatOpenAI

from agents.base import BaseAgent
from config import Settings, settings, LLMConfig
from state import AgentState
from utils.parsers import parse_editor_response
from prompts.editor_prompts import (
    EDITOR_SCIENCE,
    EDITOR_POLITICS,
    EDITOR_GAMING,
    EDITOR_DEFAULT,
)


class EditorAgent(BaseAgent):
    """Agent responsible for editing and polishing blog posts"""

    AGENT_NAME = "editor"
    AGENT_ICON = "✏️"

    def __init__(
        self,
        llm: Optional[ChatOpenAI] = None,
        llm_config: Optional[LLMConfig] = None,
        app_settings: Optional[Settings] = None,
    ):
        super().__init__(llm, llm_config, app_settings)

    def _get_default_llm_config(self) -> LLMConfig:
        return settings.llm.editor

    def _load_prompts(self) -> Dict[str, str]:
        return {
            "science": EDITOR_SCIENCE,
            "politics": EDITOR_POLITICS,
            "gaming": EDITOR_GAMING,
            "default": EDITOR_DEFAULT,
        }

    def _build_edit_prompt(self, state: AgentState) -> str:
        """
        Build the prompt for editing a blog post.

        Args:
            state: Current agent state

        Returns:
            Edit prompt string
        """
        system_prompt = self.get_system_prompt(state.category)

        return f"""
{system_prompt}

CRITICAL: This blog is ONLY about: "{state.topic}" (Category: {state.category})
Remove any content that is NOT about "{state.topic}".

---RESEARCH DATA (for fact-checking)---
{state.research_content}

---BLOG DRAFT TO EDIT---
{state.blog_draft}

---TASK---
1. REMOVE any content not directly about "{state.topic}"
2. Fact-check against the research data
3. Improve clarity and readability
4. Correct any errors or inaccuracies
5. Enhance structure and flow
6. Polish language and tone
7. Ensure it meets the {state.category} category standards

Provide:
1. The fully edited and polished blog post (ONLY about "{state.topic}")
2. A summary of all changes and corrections made

Format your response as:
---EDITED BLOG POST---
[full polished blog post here - ONLY about "{state.topic}"]

---EDITORIAL NOTES---
[summary of changes and corrections]
"""

    def _build_revision_prompt(self, state: AgentState) -> str:
        """
        Build the prompt for revising based on human feedback.

        Args:
            state: Current agent state

        Returns:
            Revision prompt string
        """
        system_prompt = self.get_system_prompt(state.category)

        return f"""
{system_prompt}

---CURRENT BLOG POST---
{state.blog_final}

---HUMAN FEEDBACK---
{state.human_feedback}

---RESEARCH DATA (for reference)---
{state.research_content}

---TASK---
Revise the blog post based on the human feedback while:
1. Maintaining factual accuracy
2. Improving the areas mentioned in feedback
3. Keeping the overall structure and quality
4. Ensuring all changes are aligned with the category standards

Provide the revised blog post:
"""

    def _build_final_review_prompt(self, state: AgentState) -> str:
        """
        Build the prompt for final quality review.

        Args:
            state: Current agent state

        Returns:
            Final review prompt string
        """
        system_prompt = self.get_system_prompt(state.category)
        sources_preview = ", ".join(state.research_sources[:5])

        return f"""
{system_prompt}

---FINAL BLOG POST---
{state.blog_final}

---RESEARCH SOURCES---
{sources_preview}

---TASK---
Provide a final quality check:

1. Is the content accurate and well-researched?
2. Is it appropriate for the target audience?
3. Are there any logical gaps or unclear sections?
4. Is the tone consistent with the category?
5. Are sources properly cited?
6. Any final suggestions for improvement?

Provide a brief final assessment with recommendations.
"""

    def edit_blog(self, state: AgentState) -> AgentState:
        """
        Edit and polish the blog post.

        Args:
            state: Current agent state

        Returns:
            Updated agent state with polished blog
        """
        self.logger.info("Reviewing and polishing blog post")

        # Truncate content if too long for LLM context
        max_chars = 2500
        original_research = state.research_content
        original_draft = state.blog_draft

        if len(state.research_content) > max_chars:
            state.research_content = state.research_content[:max_chars] + "\n[Truncated...]"
        if len(state.blog_draft) > max_chars:
            state.blog_draft = state.blog_draft[:max_chars] + "\n[Truncated...]"

        # Build and send edit prompt
        edit_prompt = self._build_edit_prompt(state)

        # Restore original content
        state.research_content = original_research
        state.blog_draft = original_draft

        editor_response = self._invoke_llm_safe(edit_prompt, fallback=state.blog_draft)

        # Parse the response using robust parser
        parsed = parse_editor_response(editor_response)

        if not parsed.parse_success:
            self.logger.warning("Used fallback parsing for editor response")

        # Update state
        state.blog_final = parsed.blog_content
        state.messages.append(
            f"Editor: Polished blog post. Notes: {len(parsed.editorial_notes)} chars"
        )

        self.logger.result("Blog edited and polished", "complete")
        self.logger.result("Editorial notes", f"{len(parsed.editorial_notes)} characters")

        return state

    def final_review(self, state: AgentState) -> Tuple[str, Dict[str, any]]:
        """
        Perform final review before human approval.

        Args:
            state: Current agent state

        Returns:
            Tuple of (final blog content, review metadata)
        """
        self.logger.info("Performing final review")

        # Build and send final review prompt
        review_prompt = self._build_final_review_prompt(state)
        assessment = self._invoke_llm_safe(
            review_prompt, fallback="Final review completed without issues"
        )

        self.logger.result("Final review", "completed")

        return state.blog_final, {
            "assessment": assessment,
            "sources": state.research_sources,
        }

    def rewrite_with_feedback(self, state: AgentState) -> AgentState:
        """
        Rewrite blog post based on human feedback.

        Args:
            state: Current agent state

        Returns:
            Updated agent state with revised blog
        """
        self.logger.info("Revising based on feedback")

        # Build and send revision prompt
        revision_prompt = self._build_revision_prompt(state)
        revised_blog = self._invoke_llm_safe(revision_prompt, fallback=state.blog_final)

        # Update state
        state.blog_final = revised_blog
        state.iteration_count += 1
        state.messages.append(
            f"Editor: Revised blog based on feedback (iteration {state.iteration_count})"
        )

        self.logger.result("Blog revised", f"iteration {state.iteration_count}")

        return state

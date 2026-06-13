"""
Writer Agent - Transforms research into engaging blog content
"""

import os
from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.messages import HumanMessage
from state import AgentState, WriterOutput
from prompts.writer_prompts import (
    WRITER_SCIENCE, WRITER_POLITICS, WRITER_GAMING, WRITER_DEFAULT
)


class WriterAgent:
    """Agent responsible for writing blog posts from research"""
    
    def __init__(self):
        self.llm = HuggingFaceEndpoint(
            repo_id="meta-llama/Llama-2-7b-chat-hf",
            huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
            temperature=0.7
        )
        
        self.prompts = {
            "science": WRITER_SCIENCE,
            "politics": WRITER_POLITICS,
            "gaming": WRITER_GAMING,
        }
    
    def get_system_prompt(self, category: str) -> str:
        """Get appropriate system prompt based on category"""
        category_lower = category.lower()
        return self.prompts.get(category_lower, WRITER_DEFAULT)
    
    def write_blog(self, state: AgentState) -> AgentState:
        """Write a blog post based on research"""
        print(f"\n✍️  WRITER: Creating blog post on '{state.topic}'")
        
        system_prompt = self.get_system_prompt(state.category)
        
        writing_prompt = f"""
{system_prompt}

---RESEARCH DATA---
{state.research_content}

---TASK---
Write an engaging, well-structured blog post about: {state.topic}

Guidelines:
- Target audience: {self._get_audience(state.category)}
- Make it informative but accessible
- Use the research data provided
- Include sources at the end
- Length: 1500-2500 words
- Make it compelling and keep readers engaged

Write the blog post now:
"""
        
        try:
            messages = [
                HumanMessage(content=writing_prompt)
            ]
            
            response = self.llm.invoke(messages)
            blog_draft = response.content
        except Exception as e:
            print(f"Writing error: {e}")
            blog_draft = f"# {state.topic}\n\n{state.research_content}"
        
        state.blog_draft = blog_draft
        state.messages.append(f"Writer: Created blog draft ({len(blog_draft)} characters)")
        
        print(f"  ✓ Blog draft created ({len(blog_draft)} characters)")
        
        return state
    
    def _get_audience(self, category: str) -> str:
        """Get audience description for category"""
        audiences = {
            "science": "Students, academics, and curious learners",
            "politics": "Engaged citizens and voters seeking truth",
            "gaming": "Gamers of all levels and gaming enthusiasts",
        }
        return audiences.get(category.lower(), "General readers")
    
    def rewrite_with_feedback(self, state: AgentState) -> AgentState:
        """Rewrite blog post based on human feedback"""
        print(f"\n✍️  WRITER: Revising based on feedback")
        
        system_prompt = self.get_system_prompt(state.category)
        
        revision_prompt = f"""
{system_prompt}

---ORIGINAL BLOG POST---
{state.blog_draft}

---HUMAN FEEDBACK---
{state.human_feedback}

---TASK---
Revise the blog post based on the human feedback provided above. 
Incorporate their suggestions and make improvements.
Keep the essence but enhance based on feedback.

Revised blog post:
"""
        
        try:
            messages = [
                HumanMessage(content=revision_prompt)
            ]
            
            response = self.llm.invoke(messages)
            revised_blog = response.content
        except Exception as e:
            print(f"Revision error: {e}")
            revised_blog = state.blog_draft
        
        state.blog_draft = revised_blog
        state.iteration_count += 1
        state.messages.append(f"Writer: Revised blog draft based on feedback (iteration {state.iteration_count})")
        
        print(f"  ✓ Blog revised (iteration {state.iteration_count})")
        
        return state

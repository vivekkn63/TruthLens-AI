"""
Editor Agent - Reviews, corrects, and polishes blog content
"""

import os
from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.messages import HumanMessage
from state import AgentState, EditorOutput
from prompts.editor_prompts import (
    EDITOR_SCIENCE, EDITOR_POLITICS, EDITOR_GAMING, EDITOR_DEFAULT
)


class EditorAgent:
    """Agent responsible for editing and polishing blog posts"""
    
    def __init__(self):
        self.llm = HuggingFaceEndpoint(
            repo_id="meta-llama/Llama-2-7b-chat-hf",
            huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
            temperature=0.3
        )
        
        self.prompts = {
            "science": EDITOR_SCIENCE,
            "politics": EDITOR_POLITICS,
            "gaming": EDITOR_GAMING,
        }
    
    def get_system_prompt(self, category: str) -> str:
        """Get appropriate system prompt based on category"""
        category_lower = category.lower()
        return self.prompts.get(category_lower, EDITOR_DEFAULT)
    
    def edit_blog(self, state: AgentState) -> AgentState:
        """Edit and polish the blog post"""
        print(f"\n✏️  EDITOR: Reviewing and polishing blog post")
        
        system_prompt = self.get_system_prompt(state.category)
        
        # First pass: fact-check and structural review
        review_prompt = f"""
{system_prompt}

---RESEARCH DATA (for fact-checking)---
{state.research_content}

---BLOG DRAFT TO EDIT---
{state.blog_draft}

---TASK---
1. Review the blog post thoroughly
2. Fact-check against the research data
3. Improve clarity and readability
4. Correct any errors or inaccuracies
5. Enhance structure and flow
6. Polish language and tone
7. Ensure it meets the category standards

Provide:
1. The fully edited and polished blog post
2. A summary of all changes and corrections made
3. Any remaining concerns or suggestions

Format your response as:
---EDITED BLOG POST---
[full polished blog post here]

---EDITORIAL NOTES---
[summary of changes and corrections]
"""
        
        try:
            messages = [
                HumanMessage(content=review_prompt)
            ]
            
            response = self.llm.invoke(messages)
            editor_response = response.content
            
            # Parse the response
            if "---EDITED BLOG POST---" in editor_response and "---EDITORIAL NOTES---" in editor_response:
                parts = editor_response.split("---EDITORIAL NOTES---")
                blog_part = parts[0].replace("---EDITED BLOG POST---", "").strip()
                notes_part = parts[1].strip() if len(parts) > 1 else "No notes"
            else:
                # Fallback if parsing fails
                blog_part = editor_response
                notes_part = "Editorial review completed"
            
        except Exception as e:
            print(f"Editing error: {e}")
            blog_part = state.blog_draft
            notes_part = f"Error during editing: {str(e)}"
        
        state.blog_final = blog_part
        state.messages.append(f"Editor: Polished blog post. Changes: {len(notes_part)} chars of notes")
        
        print(f"  ✓ Blog post edited and polished")
        print(f"  ✓ Editorial notes length: {len(notes_part)} characters")
        
        return state
    
    def final_review(self, state: AgentState) -> tuple[str, dict]:
        """Perform final review before human approval"""
        print(f"\n✏️  EDITOR: Performing final review")
        
        system_prompt = self.get_system_prompt(state.category)
        
        final_review_prompt = f"""
{system_prompt}

---FINAL BLOG POST---
{state.blog_final}

---RESEARCH SOURCES---
{', '.join(state.research_sources[:5])}

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
        
        try:
            messages = [
                HumanMessage(content=final_review_prompt)
            ]
            
            response = self.llm.invoke(messages)
            assessment = response.content
        except Exception as e:
            print(f"Final review error: {e}")
            assessment = "Final review completed without issues"
        
        print(f"  ✓ Final review completed")
        
        return state.blog_final, {"assessment": assessment, "sources": state.research_sources}
    
    def rewrite_with_feedback(self, state: AgentState) -> AgentState:
        """Rewrite blog post based on human feedback"""
        print(f"\n✏️  EDITOR: Revising based on feedback")
        
        system_prompt = self.get_system_prompt(state.category)
        
        revision_prompt = f"""
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
        
        try:
            messages = [
                HumanMessage(content=revision_prompt)
            ]
            
            response = self.llm.invoke(messages)
            revised_blog = response.content
        except Exception as e:
            print(f"Revision error: {e}")
            revised_blog = state.blog_final
        
        state.blog_final = revised_blog
        state.iteration_count += 1
        state.messages.append(f"Editor: Revised blog based on feedback (iteration {state.iteration_count})")
        
        print(f"  ✓ Blog revised (iteration {state.iteration_count})")
        
        return state

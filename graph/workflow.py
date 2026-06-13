"""
LangGraph Workflow - Orchestrates the multi-agent system
Implements the complete workflow: Research -> Write -> Edit -> Human Review -> Iterate if needed
"""

from langgraph.graph import StateGraph, END
from state import AgentState
from agents.researcher import ResearcherAgent
from agents.writer import WriterAgent
from agents.editor import EditorAgent


def create_workflow():
    """Create and return the LangGraph workflow"""
    
    # Initialize agents
    researcher = ResearcherAgent()
    writer = WriterAgent()
    editor = EditorAgent()
    
    # Create the workflow graph
    workflow = StateGraph(AgentState)
    
    # Define nodes
    def research_node(state: AgentState) -> AgentState:
        """Execute research phase"""
        return researcher.research(state)
    
    def write_node(state: AgentState) -> AgentState:
        """Execute writing phase"""
        return writer.write_blog(state)
    
    def edit_node(state: AgentState) -> AgentState:
        """Execute editing phase"""
        return editor.edit_blog(state)
    
    def writer_revise_node(state: AgentState) -> AgentState:
        """Writer revises based on feedback"""
        return writer.rewrite_with_feedback(state)
    
    def editor_revise_node(state: AgentState) -> AgentState:
        """Editor revises based on feedback"""
        return editor.rewrite_with_feedback(state)
    
    def human_review_node(state: AgentState) -> AgentState:
        """Prepare state for human review (this doesn't modify state in graph)"""
        return state
    
    # Add nodes to graph
    workflow.add_node("research", research_node)
    workflow.add_node("write", write_node)
    workflow.add_node("edit", edit_node)
    workflow.add_node("human_review", human_review_node)
    workflow.add_node("writer_revise", writer_revise_node)
    workflow.add_node("editor_revise", editor_revise_node)
    
    # Define edges
    workflow.add_edge("research", "write")  # Research -> Write
    workflow.add_edge("write", "edit")      # Write -> Edit
    workflow.add_edge("edit", "human_review")  # Edit -> Human Review
    
    # Conditional edges from human review
    def should_revise(state: AgentState) -> str:
        """Determine if we should revise or end"""
        if state.human_approved:
            return END
        elif state.iteration_count >= state.max_iterations:
            print("\n⚠️  Max iterations reached. Ending workflow.")
            return END
        else:
            # Determine which agent to route to based on feedback
            feedback_lower = state.human_feedback.lower()
            
            if "writing" in feedback_lower or "content" in feedback_lower or "structure" in feedback_lower:
                return "writer_revise"
            elif "edit" in feedback_lower or "spelling" in feedback_lower or "grammar" in feedback_lower or "format" in feedback_lower:
                return "editor_revise"
            else:
                # Default to editor revise for general improvements
                return "editor_revise"
    
    workflow.add_conditional_edges("human_review", should_revise)
    
    # Route revisions back to review
    workflow.add_edge("writer_revise", "edit")  # Writer revise -> Editor
    workflow.add_edge("editor_revise", "human_review")  # Editor revise -> Human Review
    
    # Set starting node
    workflow.set_entry_point("research")
    
    return workflow.compile()


def print_workflow_info():
    """Print workflow structure information"""
    print("""
╔════════════════════════════════════════════════════════════════╗
║           TRUTHLENS AI - Multi-Agent Orchestration              ║
╚════════════════════════════════════════════════════════════════╝

📊 WORKFLOW STRUCTURE:
  Research -> Write -> Edit -> [Human Review]
                                    ↓
                        ┌─ Writer Revise ─┐
                        │                 ↓
                        └─ Editor Revise ─→ Edit
                        
                        (Up to 3 iterations)

🔍 RESEARCHER:
  • Conducts thorough web research using Tavily
  • Synthesizes findings into structured research
  • Category-specific approach (Science/Politics/Gaming)

✍️  WRITER:
  • Transforms research into engaging blog post
  • Tailored writing style per category
  • 1500-2500 word blog posts

✏️  EDITOR:
  • Reviews for accuracy and clarity
  • Corrects factual errors
  • Polishes language and structure

👤 HUMAN LOOP:
  • Reviews final blog before publication
  • Can request writer or editor revisions
  • Can approve for publication

════════════════════════════════════════════════════════════════
""")
